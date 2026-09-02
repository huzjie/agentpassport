# -*- coding: utf-8 -*-
"""漂移检测：发现护照声明能力与实际行为的不一致。"""
from collections import Counter


class DriftDetector:
    """对比护照声明能力与近期实际动作，识别越权 / 能力漂移。"""

    def __init__(self, threshold=0.05):
        self.threshold = threshold
        self._observed = {}  # agent_id -> Counter(action)

    def observe(self, agent_id, action):
        self._observed.setdefault(agent_id, Counter())[action] += 1

    def check(self, passport):
        """返回漂移描述；无漂移返回 None。"""
        observed = self._observed.get(passport.agent_id)
        if not observed:
            return None
        allowed = set()
        for cap in passport.capabilities:
            allowed.update(cap.actions)
            allowed.add("*")
        total = sum(observed.values())
        unauthorized = {a: c for a, c in observed.items() if a not in allowed}
        if not unauthorized:
            return None
        ratio = sum(unauthorized.values()) / total if total else 0.0
        if ratio > self.threshold:
            return "能力漂移: %d%% 动作超出声明范围 %s" % (
                int(ratio * 100), sorted(unauthorized))
        return None
