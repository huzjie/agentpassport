# -*- coding: utf-8 -*-
"""护照签发机构（CA）：生成带指纹与签名的数字护照。"""
from datetime import datetime, timedelta, timezone

from ..crypto import sha256_any, hmac_sign, gen_id
from ..errors import PassportError
from ..models import AgentPassport, Capability
from ..semver import SemVer


class PassportAuthority:
    """负责签发、更新、吊销智能体数字护照。"""

    def __init__(self, secret, issuer="agentpassport-ca", default_ttl_days=365,
                 store=None):
        self.secret = secret
        self.issuer = issuer
        self.default_ttl_days = default_ttl_days
        self.store = store

    def issue(self, name, owner, capabilities=None, provider="", model="",
              version="1.0.0", ttl_days=None, metadata=None):
        """签发一张新护照。"""
        caps = [Capability(**c) if isinstance(c, dict) else c
                for c in (capabilities or [])]
        agent_id = gen_id("agt")
        ttl = ttl_days if ttl_days is not None else self.default_ttl_days
        expires = (datetime.now(timezone.utc) + timedelta(days=ttl)).isoformat()
        p = AgentPassport(
            agent_id=agent_id, name=name, owner=owner, provider=provider,
            model=model, version=version, capabilities=caps, issuer=self.issuer,
            expires_at=expires, metadata=metadata or {},
        )
        self._sign(p)
        if self.store:
            self.store.upsert(p)
        return p

    def renew(self, passport, ttl_days=None):
        """续期护照（重新签发新有效期与指纹）。"""
        ttl = ttl_days if ttl_days is not None else self.default_ttl_days
        passport.expires_at = (
            datetime.now(timezone.utc) + timedelta(days=ttl)).isoformat()
        self._sign(passport)
        if self.store:
            self.store.upsert(passport)
        return passport

    def revoke(self, passport_or_id, reason=""):
        """吊销护照。"""
        agent_id = (passport_or_id.agent_id if isinstance(passport_or_id, AgentPassport)
                    else passport_or_id)
        if self.store:
            self.store.set_status(agent_id, "revoked")
        return agent_id

    def _sign(self, p: AgentPassport):
        p.fingerprint = sha256_any(p.content_payload())
        p.signature = hmac_sign(self.secret, p.fingerprint)
        return p

    def verify_signature(self, p: AgentPassport) -> bool:
        """校验护照指纹与签名是否一致。"""
        if not p.fingerprint or not p.signature:
            return False
        recomputed = sha256_any(p.content_payload())
        from ..crypto import constant_time_eq
        return constant_time_eq(recomputed, p.fingerprint) and constant_time_eq(
            hmac_sign(self.secret, recomputed), p.signature)
