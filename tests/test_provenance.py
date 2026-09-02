# -*- coding: utf-8 -*-
from agentpassport.provenance import AttestationChain, ReplayGuard


def test_chain_verify():
    chain = AttestationChain()
    r1 = chain.record("a1", "read")
    r2 = chain.record("a1", "read")
    r3 = chain.record("a1", "read")
    ok, idx = chain.verify_chain([r1, r2, r3])
    assert ok is True and idx == -1


def test_chain_break():
    chain = AttestationChain()
    r1 = chain.record("a1", "read")
    r2 = chain.record("a1", "read")
    r3 = chain.record("a1", "read")
    # 篡改 r2 的 parent_hash
    r2.parent_hash = "0" * 64
    ok, idx = chain.verify_chain([r1, r2, r3])
    assert ok is False and idx == 1


def test_replay_guard():
    g = ReplayGuard()
    assert g.check_and_mark("n1") is True
    assert g.check_and_mark("n1") is False
    assert g.check_and_mark("n2") is True
