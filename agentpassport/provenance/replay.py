# -*- coding: utf-8 -*-
"""重放防护：基于 nonce 去重，阻止同一证明被重复提交。"""
import time


class ReplayGuard:
    """维护已见 nonce 集合，超时自动清理。"""

    def __init__(self, window_sec=3600, max_entries=100000):
        self.window_sec = window_sec
        self.max_entries = max_entries
        self._seen = {}  # nonce -> expiry_ts

    def check_and_mark(self, nonce) -> bool:
        """返回 True 表示首次出现（允许通过），False 表示重放。"""
        now = time.time()
        self._gc(now)
        if nonce in self._seen:
            return False
        self._seen[nonce] = now + self.window_sec
        return True

    def _gc(self, now):
        if len(self._seen) > self.max_entries:
            expired = [k for k, v in self._seen.items() if v < now]
            for k in expired:
                del self._seen[k]
