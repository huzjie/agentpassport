# -*- coding: utf-8 -*-
from agentpassport.policy import PolicyEngine
from agentpassport.models import AgentPassport


def _passport(caps):
    return AgentPassport(agent_id="a1", name="x", owner="o", capabilities=caps)


def test_default_deny():
    eng = PolicyEngine(default="deny")
    p = _passport([])
    dec = eng.evaluate(p, "read")
    assert dec.allowed is False


def test_allow_with_capability():
    eng = PolicyEngine(default="deny")
    from agentpassport.models import Capability
    p = _passport([Capability(name="read-data", actions=["read"])])
    dec = eng.evaluate(p, "read")
    assert dec.allowed is True


def test_blocklist():
    eng = PolicyEngine(default="deny")
    from agentpassport.models import Capability
    p = _passport([Capability(name="read-data", actions=["*"])])
    dec = eng.evaluate(p, "delete-production")
    assert dec.allowed is False
