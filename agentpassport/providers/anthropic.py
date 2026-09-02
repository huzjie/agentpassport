# -*- coding: utf-8 -*-
"""Anthropic Claude Provider（Messages API）。"""
import json
import urllib.error
import urllib.request

from .base import Provider, ProviderResult


class AnthropicProvider(Provider):
    name = "anthropic"

    def complete(self, prompt, system="", temperature=0.0, max_tokens=1024) -> ProviderResult:
        url = (self.base_url or "https://api.anthropic.com").rstrip("/") + "/v1/messages"
        payload = {
            "model": self.model or "claude-sonnet-5",
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        }
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("x-api-key", self.api_key)
        req.add_header("anthropic-version", "2023-06-01")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise RuntimeError("Anthropic HTTP %s: %s" % (e.code,
                                                          e.read().decode("utf-8", "replace")[:300]))
        text = "".join(b.get("text", "") for b in body.get("content", []))
        return ProviderResult(text=text, model=body.get("model", self.model),
                              usage=body.get("usage", {}), raw=body)
