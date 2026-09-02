# -*- coding: utf-8 -*-
"""agentpassport Python SDK：标准库 urllib 实现的轻量客户端。"""
import json
import urllib.error
import urllib.request


class Client:
    """访问 agentpassport HTTP 控制面的客户端。"""

    def __init__(self, base_url="http://127.0.0.1:8420", timeout=30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method, path, payload=None):
        url = self.base_url + path
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else None
        except urllib.error.HTTPError as e:
            raise RuntimeError("HTTP %s %s: %s" % (e.code, path,
                                                   e.read().decode("utf-8", "replace")[:200]))

    def health(self):
        return self._request("GET", "/healthz")

    def doctor(self):
        return self._request("GET", "/doctor")

    def list_passports(self):
        return self._request("GET", "/passports")

    def issue(self, name, owner, capabilities=None, provider="", model=""):
        return self._request("POST", "/passports", {
            "name": name, "owner": owner, "capabilities": capabilities,
            "provider": provider, "model": model,
        })

    def get_passport(self, agent_id):
        return self._request("GET", "/passports/" + agent_id)

    def revoke(self, agent_id, reason=""):
        return self._request("POST", "/passports/%s/revoke" % agent_id,
                             {"reason": reason})

    def audit(self, agent_id, action, context=None):
        return self._request("POST", "/audit", {
            "agent_id": agent_id, "action": action, "context": context or {},
        })

    def verify_chain(self):
        return self._request("GET", "/audit/verify")

    def provenance(self, agent_id):
        return self._request("GET", "/provenance/" + agent_id)

    def record_provenance(self, agent_id, action, inputs=None, outputs=None,
                          tool="", duration_ms=0):
        return self._request("POST", "/provenance", {
            "agent_id": agent_id, "action": action, "inputs": inputs,
            "outputs": outputs, "tool": tool, "duration_ms": duration_ms,
        })

    def topology(self):
        return self._request("GET", "/channels/topology")

    def evaluate(self, agent_id, action, context=None):
        return self._request("POST", "/policy/evaluate", {
            "agent_id": agent_id, "action": action, "context": context or {},
        })
