# -*- coding: utf-8 -*-
"""Prometheus 文本格式指标（零依赖）。"""
import threading


class Metrics:
    """计数器 / 直方图风格的轻量指标，导出 Prometheus 文本格式。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._counters = {}
        self._gauges = {}

    def inc(self, name, labels=None, value=1):
        key = (name, tuple(sorted((labels or {}).items())))
        with self._lock:
            self._counters[key] = self._counters.get(key, 0) + value

    def set_gauge(self, name, value, labels=None):
        key = (name, tuple(sorted((labels or {}).items())))
        with self._lock:
            self._gauges[key] = value

    def render(self):
        lines = []
        with self._lock:
            for (name, labels), val in sorted(self._counters.items()):
                lines.append("%s%s %d" % (name, _fmt_labels(labels), val))
            for (name, labels), val in sorted(self._gauges.items()):
                lines.append("%s%s %g" % (name, _fmt_labels(labels), val))
        return "\n".join(lines) + ("\n" if lines else "")


def _fmt_labels(labels):
    if not labels:
        return ""
    return "{" + ",".join('%s="%s"' % (k, v) for k, v in labels) + "}"
