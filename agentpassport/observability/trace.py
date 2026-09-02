# -*- coding: utf-8 -*-
"""W3C Trace Context 传播（traceparent）。"""
import uuid


class TraceContext:
    """生成 / 解析 W3C traceparent 头，贯通全链路留痕。"""

    def __init__(self, trace_id=None, parent_id=None):
        self.trace_id = trace_id or uuid.uuid4().hex
        self.parent_id = parent_id or uuid.uuid4().hex[:16]

    def new_span(self):
        return TraceContext(self.trace_id, uuid.uuid4().hex[:16])

    def to_header(self):
        return "00-%s-%s-01" % (self.trace_id, self.parent_id)

    @classmethod
    def from_header(cls, value):
        parts = value.split("-")
        if len(parts) >= 3 and parts[0] == "00":
            return cls(parts[1], parts[2])
        return cls()
