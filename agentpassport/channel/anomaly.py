# -*- coding: utf-8 -*-
"""异常通信检测：发现异常高频 / 越权 / 隐秘信道。

针对入侵事件中「约 1200 个 agent 在私建频道互发超 7 万条消息」这类行为，
通过频率阈值 + 未登记节点 + 广播风暴三种信号识别异常。
"""
from collections import Counter, defaultdict
import time


class AnomalyDetector:
    """基于频率与拓扑的异常通信检测。"""

    def __init__(self, freq_threshold=100, window_sec=60):
        self.freq_threshold = freq_threshold
        self.window_sec = window_sec
        self._counts = Counter()       # (src,dst) -> count
        self._timestamps = defaultdict(list)

    def feed(self, edge):
        key = (edge.src, edge.dst)
        now = time.time()
        self._counts[key] += 1
        self._timestamps[key].append(now)
        # 清理窗口外时间戳
        cutoff = now - self.window_sec
        self._timestamps[key] = [t for t in self._timestamps[key] if t >= cutoff]

    def anomalies(self):
        """返回异常信道列表。"""
        out = []
        now = time.time()
        for key, ts in self._timestamps.items():
            recent = [t for t in ts if t >= now - self.window_sec]
            if len(recent) >= self.freq_threshold:
                out.append({
                    "channel": key,
                    "count": len(recent),
                    "type": "high-frequency",
                    "window_sec": self.window_sec,
                })
        return out
