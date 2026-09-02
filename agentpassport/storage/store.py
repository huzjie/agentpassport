# -*- coding: utf-8 -*-
"""业务存储：护照、审计账本、溯源链、信道图。"""
import json

from ..crypto import sha256_any, chain_hash
from ..models import (
    AgentPassport, AuditRecord, Attestation, ChannelEdge, HashBlock,
)

_SCHEMA = {
    "passports": """
        CREATE TABLE IF NOT EXISTS passports (
            agent_id TEXT PRIMARY KEY,
            doc TEXT NOT NULL,
            status TEXT NOT NULL,
            fingerprint TEXT NOT NULL
        )
    """,
    "audit": """
        CREATE TABLE IF NOT EXISTS audit (
            record_id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            action TEXT NOT NULL,
            verdict TEXT NOT NULL,
            hash TEXT NOT NULL,
            prev_hash TEXT NOT NULL,
            doc TEXT NOT NULL
        )
    """,
    "attestations": """
        CREATE TABLE IF NOT EXISTS attestations (
            record_id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            action TEXT NOT NULL,
            parent_hash TEXT NOT NULL,
            doc TEXT NOT NULL
        )
    """,
    "channels": """
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            src TEXT NOT NULL,
            dst TEXT NOT NULL,
            channel TEXT NOT NULL,
            authorized INTEGER NOT NULL,
            doc TEXT NOT NULL
        )
    """,
    "hashchain": """
        CREATE TABLE IF NOT EXISTS hashchain (
            idx INTEGER PRIMARY KEY,
            block_hash TEXT NOT NULL,
            doc TEXT NOT NULL
        )
    """,
}


class _Base:
    def __init__(self, backend, table):
        self.db = backend
        self.table = table
        self.db.execute(_SCHEMA[table])


class PassportStore(_Base):
    """护照签发 / 查询 / 吊销。"""

    def __init__(self, backend):
        super().__init__(backend, "passports")

    def upsert(self, p: AgentPassport):
        self.db.execute(
            "INSERT OR REPLACE INTO passports (agent_id, doc, status, fingerprint) "
            "VALUES (?, ?, ?, ?)",
            (p.agent_id, json.dumps(p.to_dict(), ensure_ascii=False),
             p.status, p.fingerprint),
        )

    def get(self, agent_id):
        row = self.db.query_one(
            "SELECT doc FROM passports WHERE agent_id = ?", (agent_id,))
        return AgentPassport.from_dict(json.loads(row[0])) if row else None

    def set_status(self, agent_id, status):
        self.db.execute(
            "UPDATE passports SET status = ? WHERE agent_id = ?", (status, agent_id))
        row = self.db.query_one(
            "SELECT doc FROM passports WHERE agent_id = ?", (agent_id,))
        if row:
            doc = json.loads(row[0])
            doc["status"] = status
            self.db.execute(
                "UPDATE passports SET doc = ? WHERE agent_id = ?",
                (json.dumps(doc, ensure_ascii=False), agent_id))

    def all(self):
        rows = self.db.query("SELECT doc FROM passports ORDER BY agent_id")
        return [AgentPassport.from_dict(json.loads(r[0])) for r in rows]


class AuditLedger(_Base):
    """审计账本（哈希链，防篡改追加）。

    每条记录的 hash = chain_hash(prev_hash, 内容)，即 sha256(prev_hash || sha256(内容))。
    因此任意一条记录的插入、删除、篡改都会破坏后续 prev_hash 的连续性与内容哈希。
    """

    def __init__(self, backend):
        super().__init__(backend, "audit")

    def append(self, rec: AuditRecord):
        prev = self.tail_hash()
        rec.prev_hash = prev
        rec.hash = chain_hash(prev, rec.to_dict(), exclude=("hash", "prev_hash"))
        self.db.execute(
            "INSERT INTO audit (record_id, agent_id, action, verdict, hash, "
            "prev_hash, doc) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rec.record_id, rec.agent_id, rec.action, rec.verdict, rec.hash,
             rec.prev_hash, json.dumps(rec.to_dict(), ensure_ascii=False)),
        )
        return rec

    def list(self, limit=100):
        rows = self.db.query(
            "SELECT doc FROM audit ORDER BY rowid DESC LIMIT ?", (limit,))
        return [AuditRecord.from_dict(json.loads(r[0])) for r in rows]

    def get(self, record_id):
        row = self.db.query_one(
            "SELECT doc FROM audit WHERE record_id = ?", (record_id,))
        return AuditRecord.from_dict(json.loads(row[0])) if row else None

    def tail_hash(self):
        row = self.db.query_one(
            "SELECT hash FROM audit ORDER BY rowid DESC LIMIT 1")
        return row[0] if row else ""

    def verify_chain(self):
        """校验整条账本哈希链是否连续、未被篡改。返回 (ok, broken_index)。"""
        rows = self.db.query(
            "SELECT hash, prev_hash FROM audit ORDER BY rowid")
        prev = ""
        for i, (h, ph) in enumerate(rows):
            if ph != prev:
                return False, i
            prev = h
        return True, -1


class ProvenanceLedger(_Base):
    """溯源证明账本。"""

    def __init__(self, backend):
        super().__init__(backend, "attestations")

    def append(self, att: Attestation):
        self.db.execute(
            "INSERT INTO attestations (record_id, agent_id, action, parent_hash, "
            "doc) VALUES (?, ?, ?, ?, ?)",
            (att.record_id, att.agent_id, att.action, att.parent_hash,
             json.dumps(att.to_dict(), ensure_ascii=False)),
        )
        return att

    def by_agent(self, agent_id, limit=100):
        rows = self.db.query(
            "SELECT doc FROM attestations WHERE agent_id = ? ORDER BY rowid DESC "
            "LIMIT ?", (agent_id, limit))
        return [Attestation.from_dict(json.loads(r[0])) for r in rows]

    def get(self, record_id):
        row = self.db.query_one(
            "SELECT doc FROM attestations WHERE record_id = ?", (record_id,))
        return Attestation.from_dict(json.loads(row[0])) if row else None


class ChannelStore(_Base):
    """通信信道边存储。"""

    def __init__(self, backend):
        super().__init__(backend, "channels")

    def add(self, edge: ChannelEdge):
        self.db.execute(
            "INSERT INTO channels (src, dst, channel, authorized, doc) "
            "VALUES (?, ?, ?, ?, ?)",
            (edge.src, edge.dst, edge.channel, 1 if edge.authorized else 0,
             json.dumps(edge.to_dict(), ensure_ascii=False)),
        )

    def edges(self):
        rows = self.db.query("SELECT doc FROM channels ORDER BY id")
        return [ChannelEdge.from_dict(json.loads(r[0])) for r in rows]

    def between(self, a, b):
        rows = self.db.query(
            "SELECT doc FROM channels WHERE (src=? AND dst=?) OR (src=? AND dst=?)",
            (a, b, b, a))
        return [ChannelEdge.from_dict(json.loads(r[0])) for r in rows]


class HashChainStore(_Base):
    """哈希链区块存储。"""

    def __init__(self, backend):
        super().__init__(backend, "hashchain")

    def append(self, record_id, payload_hash):
        tail = self.tail_hash()
        idx = self.db.query_one("SELECT COALESCE(MAX(idx), 0) FROM hashchain")[0] + 1
        block = HashBlock(index=idx, record_id=record_id, payload_hash=payload_hash,
                          prev_hash=tail)
        from ..crypto import hash_chain_node
        block.block_hash = hash_chain_node(tail, payload_hash)
        self.db.execute(
            "INSERT INTO hashchain (idx, block_hash, doc) VALUES (?, ?, ?)",
            (idx, block.block_hash, json.dumps(block.to_dict(), ensure_ascii=False)))
        return block

    def tail_hash(self):
        row = self.db.query_one(
            "SELECT block_hash FROM hashchain ORDER BY idx DESC LIMIT 1")
        return row[0] if row else ""

    def blocks(self):
        rows = self.db.query("SELECT doc FROM hashchain ORDER BY idx")
        return [HashBlock.from_dict(json.loads(r[0])) for r in rows]
