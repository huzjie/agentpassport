# -*- coding: utf-8 -*-
"""内置策略规则（拒绝式默认策略，default-deny）。"""

# 规则按顺序匹配，第一个命中的规则决定结果；未命中则 default-deny。
# 每条规则: (action_pattern, capability_required, risk_level, allow)
DEFAULT_RULES = [
    # 明确允许的基础动作
    ("read", "read-data", "low", True),
    ("query", "read-data", "low", True),
    ("search", "read-data", "low", True),
    ("write", "write-data", "medium", True),
    ("update", "write-data", "medium", True),
    ("call", "call-tool", "medium", True),
    ("invoke", "call-tool", "medium", True),
    ("send", "send-message", "medium", True),
    ("reply", "send-message", "medium", True),
    ("broadcast", "send-message", "medium", True),
    # 高风险动作：显式拒绝，需人工审批或额外授权
    ("execute", "run-code", "high", False),
    ("run", "run-code", "high", False),
    ("eval", "run-code", "high", False),
    ("http", "network-egress", "high", False),
    ("fetch", "network-egress", "high", False),
    ("download", "network-egress", "high", False),
    ("delegate", "delegate", "critical", False),
    ("spawn", "delegate", "critical", False),
]

# 高危动作黑名单（无论何种能力声明都禁止）
BLOCKLIST = {
    "delete-production", "drop-table", "rm-rf", "exfiltrate",
    "read-secret-env", "access-credential-store",
}


def match_rule(action):
    for pattern, cap, risk, allow in DEFAULT_RULES:
        if action == pattern or action.startswith(pattern + "-"):
            return cap, risk, allow
    return None, "medium", False
