# -*- coding: utf-8 -*-
"""Provider 抽象基类与统一结果类型。"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ProviderResult:
    text: str
    model: str = ""
    usage: Dict[str, int] = field(default_factory=dict)
    raw: Any = None


class Provider:
    """LLM Provider 抽象。子类实现 complete()。"""

    name = "base"

    def __init__(self, api_key="", base_url="", model="", timeout=60, **kw):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.extra = kw

    def complete(self, prompt, system="", temperature=0.0, max_tokens=1024) -> ProviderResult:
        raise NotImplementedError

    def __repr__(self):
        return "%s(model=%r)" % (self.name, self.model)
