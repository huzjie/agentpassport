# -*- coding: utf-8 -*-
"""合规框架检查：EU AI Act、中国智能体治理、可配置的自定义框架。"""
from .engine import Decision


def check(framework, passport, action, context):
    """按合规框架做最小检查。返回 Decision 或 None（表示不适用）。"""
    fw = framework.lower()
    if fw in ("eu-ai-act", "eu_ai_act", "eu"):
        return _eu_ai_act(passport, action)
    if fw in ("cn-agent-governance", "cn", "china"):
        return _cn_governance(passport, action)
    return None


def _eu_ai_act(passport, action):
    # 高风险 AI 系统要求人类监督 + 日志留存
    high_risk = {"execute", "run", "eval", "delegate", "spawn"}
    if action in high_risk and not passport.metadata.get("human_oversight"):
        return Decision(False, "EU AI Act: 高风险动作需人类监督", "eu-ai-act")
    return None


def _cn_governance(passport, action):
    # 中国智能体治理：数字护照 + 循环审计 + 全链路留痕
    if not passport.fingerprint:
        return Decision(False, "中国智能体治理: 缺少数字护照指纹", "cn-governance")
    if action in ("delegate", "spawn") and not passport.metadata.get("registered"):
        return Decision(False, "中国智能体治理: 委派需登记备案", "cn-governance")
    return None
