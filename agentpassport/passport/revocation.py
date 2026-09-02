# -*- coding: utf-8 -*-
"""吊销列表（CRL 风格）：维护被吊销护照的 ID 与原因。"""
import json
import time


class RevocationList:
    """内存 + 可选文件持久化的吊销列表。"""

    def __init__(self, path=None):
        self.path = path
        self._revoked = {}  # agent_id -> (reason, ts)
        if path:
            self._load()

    def revoke(self, agent_id, reason=""):
        self._revoked[agent_id] = (reason, time.time())
        self._save()

    def is_revoked(self, agent_id) -> bool:
        return agent_id in self._revoked

    def reason(self, agent_id):
        return self._revoked.get(agent_id, ("", 0))[0]

    def all(self):
        return dict(self._revoked)

    def _load(self):
        from pathlib import Path
        p = Path(self.path)
        if p.exists():
            try:
                self._revoked = json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self._revoked = {}

    def _save(self):
        if not self.path:
            return
        from pathlib import Path
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.path).write_text(json.dumps(self._revoked, ensure_ascii=False),
                                   encoding="utf-8")
