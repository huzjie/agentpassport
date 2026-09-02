# -*- coding: utf-8 -*-
"""SQLite 后端（标准库 sqlite3，零依赖）。"""
import sqlite3
from contextlib import closing
from pathlib import Path


class SqliteBackend:
    """轻量 SQLite 封装：自动建表、可执行参数化 SQL。"""

    def __init__(self, path="data/agentpassport.db"):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

    def _conn(self):
        return sqlite3.connect(self.path)

    def execute(self, sql, params=()):
        with closing(self._conn()) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute(sql, params)
                conn.commit()
                return cur.lastrowid

    def executemany(self, sql, seq):
        with closing(self._conn()) as conn:
            with closing(conn.cursor()) as cur:
                cur.executemany(sql, seq)
                conn.commit()

    def query(self, sql, params=()):
        with closing(self._conn()) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute(sql, params)
                return cur.fetchall()

    def query_one(self, sql, params=()):
        rows = self.query(sql, params)
        return rows[0] if rows else None
