# -*- coding: utf-8 -*-
"""护照校验器：校验有效性、过期、吊销、能力授权。"""
from datetime import datetime, timezone

from ..errors import (
    PassportExpiredError, PassportInvalidError, PassportRevokedError,
    PassportError,
)
from ..models import PassportStatus
from ..semver import SemVer


class PassportVerifier:
    """对外提供护照有效性校验与能力判定。"""

    def __init__(self, authority=None, revocation=None, now=None):
        self.authority = authority
        self.revocation = revocation
        self.now = now

    def _utcnow(self):
        return self.now or datetime.now(timezone.utc)

    def validate(self, passport) -> bool:
        """校验护照是否有效（签名 / 状态 / 过期 / 吊销）。"""
        if self.authority and not self.authority.verify_signature(passport):
            raise PassportInvalidError("护照指纹或签名校验失败")
        if passport.status == PassportStatus.REVOKED.value:
            raise PassportRevokedError("护照已被吊销: " + passport.agent_id)
        if self.revocation and self.revocation.is_revoked(passport.agent_id):
            raise PassportRevokedError("护照在吊销列表中: " + passport.agent_id)
        if passport.expires_at:
            try:
                exp = datetime.fromisoformat(passport.expires_at)
            except ValueError:
                raise PassportInvalidError("无效的过期时间格式")
            if exp < self._utcnow():
                raise PassportExpiredError("护照已过期: " + passport.agent_id)
        return True

    def authorize(self, passport, action) -> bool:
        """判断护照是否被授权执行某个动作。"""
        self.validate(passport)
        for cap in passport.capabilities:
            if action in cap.actions or "*" in cap.actions:
                return True
        return False

    def has_capability(self, passport, capability_name, min_version=None) -> bool:
        self.validate(passport)
        for cap in passport.capabilities:
            if cap.name != capability_name:
                continue
            if min_version and SemVer.parse(cap.version) < SemVer.parse(min_version):
                return False
            return True
        return False
