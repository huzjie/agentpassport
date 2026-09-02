# -*- coding: utf-8 -*-
"""策略引擎：默认拒绝 + 规则匹配 + 合规校验。"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .rules import DEFAULT_RULES, BLOCKLIST, match_rule


@dataclass
class Decision:
    allowed: bool
    reason: str = ""
    rule: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


class PolicyEngine:
    """拒绝式默认策略引擎：未明确允许即拒绝。"""

    def __init__(self, rules=None, default="deny", compliance=None):
        self.rules = rules or DEFAULT_RULES
        self.default = default
        self.compliance = compliance or []
        self.policy_id = "default"

    def evaluate(self, passport, action, context=None) -> Decision:
        context = context or {}
        # 1. 高危动作黑名单
        if action in BLOCKLIST:
            return Decision(False, "动作 %r 在黑名单中" % action, "blocklist")

        # 2. 能力校验
        cap, risk, allow = match_rule(action)
        if cap is not None:
            has_cap = any(c.name == cap or "*" in c.actions
                          for c in passport.capabilities)
            if allow and not has_cap:
                return Decision(False, "缺少能力声明: %s" % cap, "capability")
            if allow and has_cap:
                return Decision(True, "已授权动作", "allow")

        # 3. 合规校验
        for framework in self.compliance:
            dec = self._check_compliance(framework, passport, action, context)
            if dec is not None and not dec.allowed:
                return dec

        # 4. 默认拒绝
        if self.default == "deny":
            return Decision(False, "未命中任何允许规则，默认拒绝", "default-deny")
        return Decision(True, "默认允许", "default-allow")

    def _check_compliance(self, framework, passport, action, context):
        from .compliance import check
        return check(framework, passport, action, context)
