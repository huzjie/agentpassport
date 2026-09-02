# -*- coding: utf-8 -*-
"""哈希与签名工具（纯标准库，零第三方依赖）。

提供 SHA-256 指纹、HMAC 签名、哈希链节点计算与常量化比较，是护照指纹、
溯源链与防篡改审计的底层基础。
"""
import hashlib
import hmac
import json
import time
import uuid

HASH = "sha256"


def sha256(data) -> str:
    """返回输入（str/bytes）的 SHA-256 十六进制摘要。"""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def sha256_any(obj) -> str:
    """对任意可 JSON 序列化对象做规范化哈希。"""
    return sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str))


def hmac_sign(secret: str, message: str) -> str:
    """用 HMAC-SHA256 生成签名。"""
    return hmac.new(secret.encode("utf-8"), message.encode("utf-8"),
                    hashlib.sha256).hexdigest()


def constant_time_eq(a: str, b: str) -> bool:
    """常数时间字符串比较，防止时序侧信道。"""
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def gen_nonce() -> str:
    """生成随机 nonce（含时间戳 + uuid）。"""
    return "%d-%s" % (int(time.time() * 1000), uuid.uuid4().hex)


def gen_id(prefix: str) -> str:
    """生成带前缀的唯一 ID。"""
    return "%s-%s" % (prefix, uuid.uuid4().hex[:16])


def hash_chain_node(prev_hash: str, payload: str) -> str:
    """计算哈希链下一个节点：sha256(prev_hash || payload)。"""
    return sha256(prev_hash + "\n" + payload)


def chain_hash(prev_hash: str, obj_dict: dict, exclude=()) -> str:
    """计算对象的链上哈希：hash_chain_node(prev_hash, sha256(内容))。

    用于审计账本 / 溯源链的一致性校验：内容哈希排除 hash、prev_hash 等链字段，
    再与上一节点哈希串联，保证「任何改动都破坏链完整性」。
    """
    content = {k: v for k, v in obj_dict.items() if k not in exclude}
    return hash_chain_node(prev_hash, sha256_any(content))
