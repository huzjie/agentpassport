# -*- coding: utf-8 -*-
"""核心数据模型（dataclass）。

定义智能体数字护照、能力声明、溯源证明、审计记录、哈希链区块与通信边。
所有模型均支持 to_dict/from_dict，可直接 JSON 序列化。
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


def now_iso() -> str:
    """当前 UTC 时间 ISO 字符串。"""
    return datetime.now(timezone.utc).isoformat()


class PassportStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"


class AuditVerdict(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class Capability:
    """能力声明：智能体被允许执行的一类动作及其权限范围。"""
    name: str
    version: str = "1.0.0"
    actions: List[str] = field(default_factory=list)
    scopes: List[str] = field(default_factory=list)
    risk: str = "medium"  # low / medium / high / critical

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Capability":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class AgentPassport:
    """智能体数字护照：身份 + 能力 + 签发信息 + 防篡改指纹。"""
    agent_id: str
    name: str
    owner: str
    provider: str = ""
    model: str = ""
    version: str = "1.0.0"
    capabilities: List[Capability] = field(default_factory=list)
    issuer: str = "agentpassport-ca"
    issued_at: str = field(default_factory=now_iso)
    expires_at: Optional[str] = None
    status: str = PassportStatus.ACTIVE.value
    fingerprint: str = ""  # 内容哈希，防篡改
    signature: str = ""    # HMAC 签名
    metadata: Dict[str, Any] = field(default_factory=dict)

    def content_payload(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("fingerprint", None)
        d.pop("signature", None)
        return d

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AgentPassport":
        caps = [Capability.from_dict(c) for c in d.get("capabilities", [])]
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        kwargs["capabilities"] = caps
        return cls(**kwargs)


@dataclass
class Attestation:
    """溯源证明：一次动作的全链路留痕（谁、何时、做什么、输入输出哈希）。"""
    record_id: str
    agent_id: str
    action: str
    inputs_hash: str
    outputs_hash: str
    timestamp: str = field(default_factory=now_iso)
    parent_hash: str = ""  # 上一个记录的哈希（形成链）
    nonce: str = ""
    tool: str = ""
    duration_ms: int = 0
    status: str = "ok"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Attestation":
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**kwargs)


@dataclass
class AuditRecord:
    """审计记录：对一次行为的合规判定结果。"""
    record_id: str
    agent_id: str
    action: str
    verdict: str = AuditVerdict.PASS.value
    reason: str = ""
    policy_id: str = ""
    timestamp: str = field(default_factory=now_iso)
    evidence: List[str] = field(default_factory=list)
    hash: str = ""
    prev_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AuditRecord":
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**kwargs)


@dataclass
class HashBlock:
    """哈希链区块。"""
    index: int
    record_id: str
    payload_hash: str
    prev_hash: str
    timestamp: str = field(default_factory=now_iso)
    block_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "HashBlock":
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**kwargs)


@dataclass
class ChannelEdge:
    """智能体间通信边（用于信道监控与拓扑校验）。"""
    src: str
    dst: str
    channel: str
    timestamp: str = field(default_factory=now_iso)
    authorized: bool = False
    payload_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ChannelEdge":
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**kwargs)
