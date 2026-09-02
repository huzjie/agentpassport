# -*- coding: utf-8 -*-
"""Provider 注册表与工厂。"""
from .mock import MockProvider
from .openai_compat import OpenAICompatProvider


_REGISTRY = {
    "mock": MockProvider,
    "openai": OpenAICompatProvider,
    "deepseek": OpenAICompatProvider,
    "qwen": OpenAICompatProvider,
    "kimi": OpenAICompatProvider,
    "glm": OpenAICompatProvider,
    "gemini": OpenAICompatProvider,
    "ollama": OpenAICompatProvider,
    "vllm": OpenAICompatProvider,
}

_DEFAULT_BASE = {
    "openai": "https://api.openai.com/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "kimi": "https://api.moonshot.cn/v1",
    "glm": "https://open.bigmodel.cn/api/paas/v4",
    "gemini": "https://generativelanguage.googleapis.com/v1beta",
    "ollama": "http://localhost:11434/v1",
    "vllm": "http://localhost:8000/v1",
}

_DEFAULT_MODEL = {
    "openai": "gpt-5.6-sol",
    "deepseek": "deepseek-v4-pro",
    "qwen": "qwen3.8-max",
    "kimi": "kimi-k3",
    "glm": "glm-5.3",
    "gemini": "gemini-3.7-flash",
    "ollama": "llama3.3",
    "vllm": "",
}


def register(name, cls):
    _REGISTRY[name] = cls


def list_providers():
    return sorted(_REGISTRY.keys())


def get_provider(name, **kw):
    if name not in _REGISTRY:
        raise ValueError("未知 Provider: %s (可用: %s)" % (name, list_providers()))
    cls = _REGISTRY[name]
    if name in _DEFAULT_BASE:
        kw.setdefault("base_url", _DEFAULT_BASE[name])
    if name in _DEFAULT_MODEL:
        kw.setdefault("model", _DEFAULT_MODEL[name])
    return cls(name=name, **kw)
