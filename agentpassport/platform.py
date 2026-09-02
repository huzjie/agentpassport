# -*- coding: utf-8 -*-
"""平台装配点：把配置、存储、护照、溯源、审计、策略、信道组装成一个 App。"""
from .config import load_config
from .policy import PolicyEngine
from .passport import PassportAuthority, PassportVerifier, RevocationList
from .provenance import AttestationChain, ReplayGuard, TamperDetector
from .audit import Auditor, ContinuousAuditor, DriftDetector
from .channel import ChannelMonitor, TopologyPolicy, AnomalyDetector
from .storage import (
    PassportStore, AuditLedger, ProvenanceLedger, ChannelStore, SqliteBackend,
)


class App:
    """agentpassport 应用装配点：统一入口，所有子系统在此组装。"""

    def __init__(self, config=None, config_path=None):
        self.config = config if config is not None else load_config(config_path)
        self._assemble()

    def _assemble(self):
        cfg = self.config
        secret = cfg.get("passport", {}).get("secret", "change-me")
        issuer = cfg.get("passport", {}).get("issuer", "agentpassport-ca")
        ttl = cfg.get("passport", {}).get("default_ttl_days", 365)

        # 存储
        backend = SqliteBackend(cfg.get("storage", {}).get("path", "data/agentpassport.db"))
        self.passport_store = PassportStore(backend)
        self.audit_ledger = AuditLedger(backend)
        self.provenance_ledger = ProvenanceLedger(backend)
        self.channel_store = ChannelStore(backend)

        # 护照
        self.authority = PassportAuthority(secret, issuer=issuer, default_ttl_days=ttl,
                                           store=self.passport_store)
        self.revocation = RevocationList()
        self.verifier = PassportVerifier(self.authority, self.revocation)

        # 策略 + 合规
        self.policy = PolicyEngine(
            default=cfg.get("policy", {}).get("default", "deny"),
            compliance=cfg.get("policy", {}).get("compliance", []),
        )

        # 溯源
        self.attestation = AttestationChain(self.provenance_ledger)
        self.replay_guard = ReplayGuard()
        self.tamper = TamperDetector(self.audit_ledger)

        # 审计 + 循环审计 + 漂移
        self.drift = DriftDetector(threshold=cfg.get("audit", {}).get("drift_threshold", 0.05))
        self.auditor = Auditor(self.policy, self.verifier, self.audit_ledger)
        self.continuous = ContinuousAuditor(
            self.verifier, self.passport_store,
            interval_sec=cfg.get("audit", {}).get("interval_sec", 3600),
            drift=self.drift,
        )

        # 信道监控
        self.channel_monitor = ChannelMonitor(
            TopologyPolicy(
                allowed=cfg.get("channel", {}).get("allowed_topologies"),
                forbid_mesh=cfg.get("channel", {}).get("forbid_p2p_mesh", True),
            ), self.channel_store)
        self.anomaly = AnomalyDetector()

        # 可观测
        from .observability import Metrics
        self.metrics = Metrics()

    def issue(self, name, owner, capabilities=None, **kw):
        return self.authority.issue(name, owner, capabilities=capabilities, **kw)

    def audit_action(self, agent_id, action, context=None):
        """端到端：加载护照 -> 审计判定 -> 记录证明。"""
        p = self.passport_store.get(agent_id)
        if not p:
            from .errors import PassportError
            raise PassportError("护照不存在: " + agent_id)
        rec = self.auditor.audit(p, action, context)
        self.drift.observe(agent_id, action)
        self.metrics.inc("agentpassport_audits_total",
                         {"verdict": rec.verdict})
        return rec

    def doctor(self):
        """健康自检。"""
        return {
            "status": "ok",
            "version": __import__("agentpassport.version", fromlist=["__version__"]).__version__,
            "passports": len(self.passport_store.all()),
            "audit_records": len(self.audit_ledger.list(100000)),
            "chain_intact": self.audit_ledger.verify_chain()[0],
        }
