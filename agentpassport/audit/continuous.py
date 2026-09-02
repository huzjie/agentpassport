# -*- coding: utf-8 -*-
"""循环审计：定时 / 事件驱动地对在册智能体做周期性重新审计与合规体检。"""
import threading
import time


class ContinuousAuditor:
    """周期性重审所有护照，检测过期 / 吊销 / 能力漂移。"""

    def __init__(self, verifier, passport_store, interval_sec=3600, drift=None,
                 callback=None):
        self.verifier = verifier
        self.store = passport_store
        self.interval_sec = interval_sec
        self.drift = drift
        self.callback = callback
        self._stop = threading.Event()
        self._thread = None
        self.last_report = []

    def run_once(self):
        """执行一轮循环审计，返回违规清单。"""
        findings = []
        for p in self.store.all():
            try:
                self.verifier.validate(p)
            except Exception as e:  # noqa: BLE001
                findings.append({"agent_id": p.agent_id, "issue": str(e)})
            if self.drift:
                d = self.drift.check(p)
                if d:
                    findings.append({"agent_id": p.agent_id, "drift": d})
        self.last_report = findings
        if self.callback:
            self.callback(findings)
        return findings

    def start(self):
        """后台线程启动循环审计。"""
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _loop(self):
        while not self._stop.is_set():
            try:
                self.run_once()
            except Exception:  # noqa: BLE001
                pass
            self._stop.wait(self.interval_sec)
