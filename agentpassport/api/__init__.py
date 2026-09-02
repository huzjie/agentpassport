# -*- coding: utf-8 -*-
"""HTTP 控制面（纯标准库 http.server，零依赖）。"""
from .server import serve, build_handler

__all__ = ["serve", "build_handler"]
