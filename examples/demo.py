# -*- coding: utf-8 -*-
"""端到端演示：签发 → 审计 → 溯源 → 信道 → 校验哈希链。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agentpassport.platform import App  # noqa: E402


def main():
    app = App()

    # 1. 签发护照
    p = app.issue("代码扫描器", "安全团队", capabilities=[
        {"name": "read-data", "actions": ["read", "search"]},
        {"name": "call-tool", "actions": ["call"]},
    ])
    print("[1] 签发护照:", p.agent_id, p.name)

    # 2. 审计允许的动作
    r1 = app.audit_action(p.agent_id, "read")
    print("[2] 审计 read ->", r1.verdict)

    # 3. 审计越权动作（应被拒绝）
    r2 = app.audit_action(p.agent_id, "delegate")
    print("[3] 审计 delegate ->", r2.verdict, "|", r2.reason)

    # 4. 溯源记录
    att = app.attestation.record(p.agent_id, "read", inputs={"q": "foo"},
                                 outputs={"n": 3})
    print("[4] 溯源记录:", att.record_id)

    # 5. 信道监控
    app.channel_monitor.record(p.agent_id, "hub", "control", authorized=True)
    print("[5] 当前拓扑:", app.channel_monitor.current_topology())

    # 6. 校验哈希链
    ok, idx = app.audit_ledger.verify_chain()
    print("[6] 哈希链完整:", ok, "断裂点:", idx)

    # 7. 循环审计
    findings = app.continuous.run_once()
    print("[7] 循环审计违规数:", len(findings))

    print("\n演示完成 ✓")


if __name__ == "__main__":
    main()
