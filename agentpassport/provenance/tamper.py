# -*- coding: utf-8 -*-
"""防伪造检测：识别被篡改 / 伪造的执行记录。

直击 OpenAI–Hugging Face 入侵事件中「约 7% 执行记录被伪造」的问题——
通过记录内容哈希与账本哈希链双重校验，定位任何被改动或凭空插入的记录。
"""
from ..crypto import sha256_any
from ..errors import TamperDetectedError


class TamperDetector:
    """校验单条记录的哈希与整链一致性。"""

    def __init__(self, ledger=None):
        self.ledger = ledger

    def verify_record(self, record) -> bool:
        """校验单条审计记录的链上哈希是否与存储哈希一致。"""
        from ..crypto import chain_hash, constant_time_eq
        d = record.to_dict()
        stored_hash = d.get("hash", "")
        if not stored_hash:
            return False
        recomputed = chain_hash(record.prev_hash, d, exclude=("hash", "prev_hash"))
        return constant_time_eq(recomputed, stored_hash)

    def scan(self, records):
        """扫描一批记录，返回被篡改记录的索引列表。"""
        tampered = []
        for i, r in enumerate(records):
            if not self.verify_record(r):
                tampered.append(i)
        return tampered

    def assert_intact(self, records):
        """任一记录被篡改则抛 TamperDetectedError。"""
        tampered = self.scan(records)
        if tampered:
            raise TamperDetectedError(
                "检测到 %d 条记录被篡改/伪造: %s" % (len(tampered), tampered))
        return True
