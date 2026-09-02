# -*- coding: utf-8 -*-
"""信道监控：记录通信边、校验拓扑、识别未授权信道。"""
from ..errors import UnauthorizedChannelError
from ..models import ChannelEdge
from .topology import TopologyPolicy


class ChannelMonitor:
    """监控智能体间通信，阻止未授权 / 越权信道。"""

    def __init__(self, policy=None, store=None):
        self.policy = policy or TopologyPolicy()
        self.store = store
        self._edges = []

    def record(self, src, dst, channel, authorized=True, payload_hash=""):
        """记录一条通信边；未授权则抛异常。"""
        edge = ChannelEdge(src=src, dst=dst, channel=channel,
                           authorized=authorized, payload_hash=payload_hash)
        if not authorized:
            raise UnauthorizedChannelError(
                "未授权信道: %s -> %s (%s)" % (src, dst, channel))
        self._edges.append(edge)
        if self.store:
            self.store.add(edge)
        return edge

    def edges(self):
        return list(self._edges)

    def current_topology(self):
        return self.policy.classify(self._edges)

    def validate_topology(self):
        """校验当前拓扑是否符合策略；不符合抛异常。"""
        topo = self.current_topology()
        if not self.policy.allowed_topology(topo):
            raise UnauthorizedChannelError(
                "当前通信拓扑 %r 超出允许范围 %s" % (topo, sorted(self.policy.allowed)))
        return topo
