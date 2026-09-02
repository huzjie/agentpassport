# -*- coding: utf-8 -*-
"""OpenAI 兼容 Provider：走 /chat/completions 接口（标准库 urllib）。"""
import json
import urllib.error
import urllib.request

from .base import Provider, ProviderResult


class OpenAICompatProvider(Provider):
    """OpenAI 兼容协议客户端（OpenAI/DeepSeek/Qwen/Kimi/GLM/Ollama/vLLM 通用）。"""

    name = "openai_compat"

    def complete(self, prompt, system="", temperature=0.0, max_tokens=1024) -> ProviderResult:
        url = self.base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        if self.api_key:
            req.add_header("Authorization", "Bearer " + self.api_key)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise RuntimeError("Provider %s HTTP %s: %s" % (self.name, e.code,
                                                            e.read().decode("utf-8", "replace")[:300]))
        text = body["choices"][0]["message"]["content"]
        usage = body.get("usage", {})
        return ProviderResult(text=text, model=body.get("model", self.model),
                              usage=usage, raw=body)
