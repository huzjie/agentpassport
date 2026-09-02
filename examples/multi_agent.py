# -*- coding: utf-8 -*-
"""多智能体协作演示：3 个智能体 + 中心 hub 拓扑 + 信道监控 + 异常检测。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agentpassport.platform import App  # noqa: E402


def main():
    app = App()

    # 签发三个智能体：规划器 / 执行器 / 审查器
    planner = app.issue("规划器", "平台", capabilities=[
        {"name": "read-data", "actions": ["read", "search"]},
        {"name": "delegate", "actions": ["delegate"]},
    ])
    executor = app.issue("执行器", "平台", capabilities=[
        {"name": "write-data", "actions": ["write", "update"]},
        {"name": "run-code", "actions": ["execute"]},
    ])
    reviewer = app.issue("审查器", "平台", capabilities=[
        {"name": "read-data", "actions": ["read", "search"]},
    ])

    print("[1] 已签发 3 个智能体:", planner.agent_id[:12], executor.agent_id[:12],
          reviewer.agent_id[:12])

    # hub 拓扑：所有智能体通过中心 hub 通信（合法）
    hub = "hub"
    for a in (planner, executor, reviewer):
        app.channel_monitor.record(a.agent_id, hub, "control", authorized=True)
        app.anomaly.feed(app.channel_monitor.edges()[-1])

    print("[2] 当前拓扑:", app.channel_monitor.current_topology())

    # 模拟异常：高频点对点通信（未授权 mesh）
    try:
        app.channel_monitor.record(executor.agent_id, reviewer.agent_id,
                                   "secret", authorized=False)
    except Exception as e:  # noqa: BLE001
        print("[3] 已阻断未授权信道:", e)

    # 审计：委派动作
    rec = app.audit_action(planner.agent_id, "delegate")
    print("[4] 规划器 delegate ->", rec.verdict, "|", rec.reason)

    # 循环审计
    findings = app.continuous.run_once()
    print("[5] 循环审计违规:", len(findings), "条")
    for f in findings:
        print("    -", f.get("agent_id", "")[:12], f.get("issue") or f.get("drift"))

    ok, idx = app.audit_ledger.verify_chain()
    print("[6] 哈希链完整:", ok, "断裂点:", idx)


if __name__ == "__main__":
    main()
