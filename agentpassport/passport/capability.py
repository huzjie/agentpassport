# -*- coding: utf-8 -*-
"""能力治理：内置标准能力模板与风险分级。"""
from ..models import Capability

STANDARD_CAPABILITIES = {
    "read-data": Capability(name="read-data", version="1.0.0",
                            actions=["read", "query", "search"],
                            scopes=["documents", "tables"], risk="low"),
    "write-data": Capability(name="write-data", version="1.0.0",
                             actions=["write", "update", "insert"],
                             scopes=["documents", "tables"], risk="medium"),
    "run-code": Capability(name="run-code", version="1.0.0",
                           actions=["execute", "run", "eval"],
                           scopes=["sandbox"], risk="high"),
    "call-tool": Capability(name="call-tool", version="1.0.0",
                            actions=["call", "invoke"], scopes=["tools"],
                            risk="medium"),
    "send-message": Capability(name="send-message", version="1.0.0",
                               actions=["send", "broadcast", "reply"],
                               scopes=["channels"], risk="medium"),
    "network-egress": Capability(name="network-egress", version="1.0.0",
                                 actions=["http", "fetch", "download"],
                                 scopes=["internet"], risk="high"),
    "delegate": Capability(name="delegate", version="1.0.0",
                           actions=["delegate", "spawn", "subcontract"],
                           scopes=["agents"], risk="critical"),
}


def standard_capability(name):
    return STANDARD_CAPABILITIES.get(name)


def all_standard():
    return list(STANDARD_CAPABILITIES.values())
