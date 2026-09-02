# -*- coding: utf-8 -*-
from agentpassport.platform import App


def test_audit_allow_and_deny(tmp_path):
    app = App({"storage": {"path": str(tmp_path / "t.db")},
               "passport": {"secret": "s", "default_ttl_days": 30, "issuer": "ca"}})
    p = app.issue("scanner", "team", capabilities=[
        {"name": "read-data", "actions": ["read"]}
    ])
    ok = app.audit_action(p.agent_id, "read")
    assert ok.verdict == "pass"
    bad = app.audit_action(p.agent_id, "delegate")
    assert bad.verdict == "fail"


def test_chain_intact(tmp_path):
    app = App({"storage": {"path": str(tmp_path / "t.db")},
               "passport": {"secret": "s", "default_ttl_days": 30, "issuer": "ca"}})
    p = app.issue("scanner", "team", capabilities=[
        {"name": "read-data", "actions": ["read"]}
    ])
    app.audit_action(p.agent_id, "read")
    app.audit_action(p.agent_id, "read")
    ok, idx = app.audit_ledger.verify_chain()
    assert ok is True and idx == -1
