# -*- coding: utf-8 -*-
"""Mock Provider：离线确定性输出，用于演示与测试（零依赖）。"""
import hashlib

from .base import Provider, ProviderResult


class MockProvider(Provider):
    """根据提示词哈希生成确定性回答，保证离线端到端可跑。"""

    name = "mock"

    def complete(self, prompt, system="", temperature=0.0, max_tokens=1024) -> ProviderResult:
        seed = hashlib.sha256((system + "\n" + prompt).encode("utf-8")).hexdigest()
        text = "MOCK-RESPONSE %s" % seed[:16]
        # 对「评估/判定」类提示词返回结构化数字
        low = prompt.lower()
        if "rating" in low or "score" in low or "评分" in prompt or "评估" in prompt:
            num = int(seed[:2], 16) % 10
            text = str(num / 10.0)
        return ProviderResult(text=text, model="mock", usage={"prompt_tokens": 8, "completion_tokens": 4})
