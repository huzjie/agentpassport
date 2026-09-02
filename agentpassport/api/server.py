# -*- coding: utf-8 -*-
"""HTTP 控制面：基于标准库 http.server 的 JSON API，零第三方依赖。"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ..platform import App


class _Handler(BaseHTTPRequestHandler):
    app = None  # 类级注入

    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self):
        ln = int(self.headers.get("Content-Length", 0))
        if ln <= 0:
            return {}
        return json.loads(self.rfile.read(ln).decode("utf-8"))

    def log_message(self, *a):
        pass

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/") or "/"
        app = self.app
        try:
            if path == "/healthz":
                return self._send(200, {"status": "ok"})
            if path == "/version":
                from ..version import __version__
                return self._send(200, {"version": __version__})
            if path == "/doctor":
                return self._send(200, app.doctor())
            if path == "/passports":
                return self._send(200, [p.to_dict() for p in app.passport_store.all()])
            if path.startswith("/passports/"):
                agent_id = path.split("/")[-1]
                p = app.passport_store.get(agent_id)
                return self._send(200 if p else 404, p.to_dict() if p else {"error": "not found"})
            if path == "/audit":
                return self._send(200, [r.to_dict() for r in app.audit_ledger.list(200)])
            if path == "/audit/verify":
                ok, idx = app.audit_ledger.verify_chain()
                return self._send(200, {"intact": ok, "broken_index": idx})
            if path.startswith("/provenance/"):
                agent_id = path.split("/")[-1]
                return self._send(200, [a.to_dict() for a in app.provenance_ledger.by_agent(agent_id)])
            if path == "/channels/topology":
                return self._send(200, {"topology": app.channel_monitor.current_topology()})
            return self._send(404, {"error": "not found"})
        except Exception as e:  # noqa: BLE001
            return self._send(500, {"error": str(e)})

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/") or "/"
        app = self.app
        data = self._json()
        try:
            if path == "/passports":
                p = app.issue(data.get("name", "agent"), data.get("owner", "unknown"),
                              capabilities=data.get("capabilities"),
                              provider=data.get("provider", ""),
                              model=data.get("model", ""))
                return self._send(201, p.to_dict())
            if path.startswith("/passports/") and path.endswith("/revoke"):
                agent_id = path.split("/")[-2]
                app.authority.revoke(agent_id, data.get("reason", ""))
                return self._send(200, {"revoked": agent_id})
            if path == "/audit":
                rec = app.audit_action(data["agent_id"], data["action"], data.get("context"))
                return self._send(200, rec.to_dict())
            if path == "/provenance":
                att = app.attestation.record(
                    data["agent_id"], data["action"],
                    inputs=data.get("inputs"), outputs=data.get("outputs"),
                    tool=data.get("tool", ""), duration_ms=data.get("duration_ms", 0))
                return self._send(201, att.to_dict())
            if path == "/channels":
                edge = app.channel_monitor.record(
                    data["src"], data["dst"], data.get("channel", "default"),
                    authorized=data.get("authorized", True))
                return self._send(201, edge.to_dict())
            if path == "/policy/evaluate":
                p = app.passport_store.get(data["agent_id"])
                if not p:
                    return self._send(404, {"error": "passport not found"})
                dec = app.policy.evaluate(p, data["action"], data.get("context", {}))
                return self._send(200, {"allowed": dec.allowed, "reason": dec.reason})
            return self._send(404, {"error": "not found"})
        except Exception as e:  # noqa: BLE001
            return self._send(400, {"error": str(e)})


def build_handler(app):
    h = type("Handler", (_Handler,), {"app": app})
    return h


def serve(app, host="127.0.0.1", port=8420):
    handler = build_handler(app)
    srv = ThreadingHTTPServer((host, port), handler)
    print("[api] listening on http://%s:%d" % (host, port))
    srv.serve_forever()
