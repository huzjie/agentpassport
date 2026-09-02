# -*- coding: utf-8 -*-
"""LLM Provider 适配器：用于护照能力评估 / 行为分析等需模型辅助的场景。"""
from .base import Provider, ProviderResult
from .registry import get_provider, register, list_providers

__all__ = ["Provider", "ProviderResult", "get_provider", "register", "list_providers"]
