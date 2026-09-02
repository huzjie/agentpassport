# -*- coding: utf-8 -*-
"""统一异常体系。"""


class AgentPassportError(Exception):
    """基础异常。"""


class ConfigError(AgentPassportError):
    """配置加载 / 校验错误。"""


class PassportError(AgentPassportError):
    """护照签发 / 校验相关错误。"""


class PassportRevokedError(PassportError):
    """护照已被吊销。"""


class PassportExpiredError(PassportError):
    """护照已过期。"""


class PassportInvalidError(PassportError):
    """护照指纹 / 签名校验失败。"""


class ProvenanceError(AgentPassportError):
    """溯源链相关错误。"""


class HashChainError(ProvenanceError):
    """哈希链断裂 / 校验失败。"""


class TamperDetectedError(ProvenanceError):
    """检测到记录被篡改 / 伪造。"""


class ReplayError(ProvenanceError):
    """检测到重放攻击。"""


class AuditError(AgentPassportError):
    """审计相关错误。"""


class PolicyDeniedError(AgentPassportError):
    """策略引擎拒绝。"""


class ChannelError(AgentPassportError):
    """信道监控相关错误。"""


class UnauthorizedChannelError(ChannelError):
    """检测到未授权的智能体间通信信道。"""


class ProviderError(AgentPassportError):
    """LLM Provider 调用错误。"""


class StorageError(AgentPassportError):
    """存储层错误。"""


__all__ = [
    "AgentPassportError", "ConfigError", "PassportError",
    "PassportRevokedError", "PassportExpiredError", "PassportInvalidError",
    "ProvenanceError", "HashChainError", "TamperDetectedError", "ReplayError",
    "AuditError", "PolicyDeniedError", "ChannelError",
    "UnauthorizedChannelError", "ProviderError", "StorageError",
]
