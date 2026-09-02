# -*- coding: utf-8 -*-
"""通信拓扑策略：约束智能体间允许的通信拓扑形态（纯标准库，零依赖）。"""
from collections import defaultdict


class TopologyPolicy:
    """定义允许的拓扑：hub / chain / broadcast / tree。禁止点对点全网 mesh。"""

    ALLOWED = {"hub", "chain", "broadcast", "tree", "star"}

    def __init__(self, allowed=None, forbid_mesh=True):
        self.allowed = set(allowed) if allowed else self.ALLOWED
        self.forbid_mesh = forbid_mesh

    def classify(self, edges):
        """基于边集合推断当前拓扑类型。"""
        if not edges:
            return "empty"
        adj = defaultdict(set)
        nodes = set()
        for e in edges:
            adj[e.src].add(e.dst)
            adj[e.dst].add(e.src)
            nodes.add(e.src)
            nodes.add(e.dst)
        n = len(nodes)
        if n <= 2:
            return "chain"
        # hub：存在一个节点连接所有其他节点
        for nd in nodes:
            if len(adj[nd]) == n - 1:
                return "hub"
        # chain：恰好 n-1 条边且无环
        if len(edges) == n - 1 and self._is_tree(nodes, adj):
            return "chain"
        return "mesh"

    @staticmethod
    def _is_tree(nodes, adj):
        seen = set()
        stack = [next(iter(nodes))]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(adj[cur] - seen)
        return len(seen) == len(nodes)

    def allowed_topology(self, topology):
        return topology in self.allowed
