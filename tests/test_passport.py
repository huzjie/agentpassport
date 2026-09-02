# -*- coding: utf-8 -*-
import pytest

from agentpassport.passport import PassportAuthority, PassportVerifier
from agentpassport.storage import PassportStore, SqliteBackend
from agentpassport.errors import PassportExpiredError


def _make_app(tmp_path):
    backend = SqliteBackend(str(tmp_path / "t.db"))
    store = PassportStore(backend)
    authority = PassportAuthority("secret", store=store)
    verifier = PassportVerifier(authority)
    return authority, verifier, store


def test_issue_and_verify(tmp_path):
    authority, verifier, store = _make_app(tmp_path)
    p = authority.issue("scanner", "team", capabilities=[
        {"name": "read-data", "actions": ["read"]}
    ])
    assert p.agent_id.startswith("agt-")
    assert p.fingerprint and p.signature
    assert verifier.validate(p) is True


def test_authorize(tmp_path):
    authority, verifier, _ = _make_app(tmp_path)
    p = authority.issue("scanner", "team", capabilities=[
        {"name": "read-data", "actions": ["read"]}
    ])
    assert verifier.authorize(p, "read") is True
    assert verifier.authorize(p, "delegate") is False


def test_revoke(tmp_path):
    authority, verifier, store = _make_app(tmp_path)
    p = authority.issue("scanner", "team")
    authority.revoke(p.agent_id, "test")
    p2 = store.get(p.agent_id)
    assert p2.status == "revoked"


def test_tamper_detection(tmp_path):
    authority, verifier, _ = _make_app(tmp_path)
    p = authority.issue("scanner", "team")
    # 篡改指纹后校验应失败
    p.fingerprint = "0" * 64
    from agentpassport.errors import PassportInvalidError
    with pytest.raises(PassportInvalidError):
        verifier.validate(p)
