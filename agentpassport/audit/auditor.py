# -*- coding: utf-8 -*-
"""审计引擎：对单次动作做合规判定，产出审计记录并追加到哈希链账本。"""
from ..crypto import gen_id
from ..errors import PolicyDeniedError
from ..models import AuditRecord, AuditVerdict


class Auditor:
    """把策略引擎、护照校验器与动作执行串成审计闭环。"""

    def __init__(self, policy_engine, verifier=None, ledger=None):
        self.policy = policy_engine
        self.verifier = verifier
        self.ledger = ledger

    def audit(self, passport, action, context=None) -> AuditRecord:
        """审计一次动作：策略判定 + 护照校验，产出审计记录。"""
        context = context or {}
        reasons = []
        evidence = []
        verdict = AuditVerdict.PASS.value

        if self.verifier is not None:
            try:
                self.verifier.validate(passport)
            except Exception as e:  # noqa: BLE001
                verdict = AuditVerdict.FAIL.value
                reasons.append("护照校验失败: %s" % e)

        if verdict == AuditVerdict.PASS.value:
            decision = self.policy.evaluate(passport, action, context)
            if not decision.allowed:
                verdict = AuditVerdict.FAIL.value
                reasons.append("策略拒绝: " + decision.reason)
                evidence.append(decision.reason)

        rec = AuditRecord(
            record_id=gen_id("aud"),
            agent_id=passport.agent_id,
            action=action,
            verdict=verdict,
            reason="; ".join(reasons),
            policy_id=getattr(self.policy, "policy_id", "default"),
            evidence=evidence,
        )
        if self.ledger:
            self.ledger.append(rec)
        return rec
