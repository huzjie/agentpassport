# -*- coding: utf-8 -*-
"""数字护照子系统：签发、校验、吊销、能力治理。"""
from .authority import PassportAuthority
from .verifier import PassportVerifier
from .revocation import RevocationList

__all__ = ["PassportAuthority", "PassportVerifier", "RevocationList"]
