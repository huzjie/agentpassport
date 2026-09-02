# -*- coding: utf-8 -*-
"""配置加载：JSON 文件 + 环境变量覆盖（零依赖，开箱即用）。

配置优先级：默认值 < config.json < 环境变量 AGENTPASSPORT_*。
环境变量用双下划线表示层级，例如 AGENTPASSPORT_AUDIT__INTERVAL_SEC。
"""
import json
import os
from pathlib import Path

from .errors import ConfigError

ENV_PREFIX = "AGENTPASSPORT_"

DEFAULTS = {
    "passport": {
        "secret": "change-me-in-production",
        "default_ttl_days": 365,
        "issuer": "agentpassport-ca",
    },
    "audit": {
        "interval_sec": 3600,
        "loop_enabled": True,
        "drift_threshold": 0.05,
    },
    "channel": {
        "allowed_topologies": ["hub", "chain", "broadcast"],
        "forbid_p2p_mesh": True,
    },
    "policy": {
        "default": "deny",
        "compliance": ["eu-ai-act", "cn-agent-governance"],
    },
    "storage": {
        "type": "sqlite",
        "path": "data/agentpassport.db",
    },
    "providers": {
        "default": "mock",
        "timeout_sec": 60,
    },
    "server": {
        "host": "127.0.0.1",
        "port": 8420,
    },
    "logging": {
        "level": "INFO",
    },
}


def _deep_merge(base, override):
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _from_env():
    """从环境变量构造覆盖字典。"""
    env = {}
    for key, val in os.environ.items():
        if not key.startswith(ENV_PREFIX):
            continue
        path = key[len(ENV_PREFIX):].lower().split("__")
        node = env
        for seg in path[:-1]:
            node = node.setdefault(seg, {})
        node[path[-1]] = _coerce(val)
    return env


def _coerce(val):
    low = val.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if val.isdigit():
        return int(val)
    try:
        return float(val)
    except ValueError:
        return val


def load_config(path=None):
    """加载配置。path 为 JSON/YAML 风格文件（这里支持 JSON 或简单 key: value）。"""
    cfg = _deep_merge(DEFAULTS, {})
    if path:
        p = Path(path)
        if p.exists():
            cfg = _deep_merge(cfg, _load_file(p))
    cfg = _deep_merge(cfg, _from_env())
    return cfg


def _load_file(p: Path):
    text = p.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return _parse_flat(text)


def _parse_flat(text):
    """极简 key: value 文本解析（兼容 config.example 的扁平写法）。"""
    data = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = _coerce(v.strip().strip('\"' + "\'"))
    return data


def default_config_path():
    here = Path(__file__).resolve().parent.parent
    for name in ("config.json", "config.yaml", "config.yml"):
        if (here / name).exists():
            return str(here / name)
    return None
