# -*- coding: utf-8 -*-
"""轻量 SemVer 2.0 解析与比较（零依赖）。"""


class SemVer:
    """语义化版本号。"""

    def __init__(self, major, minor, patch, prerelease=(), build=""):
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)
        self.prerelease = tuple(prerelease) if prerelease else ()
        self.build = build or ""

    @classmethod
    def parse(cls, text):
        if text.startswith("v"):
            text = text[1:]
        build = ""
        if "+" in text:
            text, build = text.split("+", 1)
        prerelease = ()
        if "-" in text:
            text, pre = text.split("-", 1)
            prerelease = tuple(pre.split("."))
        core = text.split(".")
        if len(core) == 1:
            core = [core[0], "0", "0"]
        elif len(core) == 2:
            core = [core[0], core[1], "0"]
        if len(core) != 3:
            raise ValueError("invalid semver: %r" % text)
        return cls(core[0], core[1], core[2], prerelease, build)

    def _cmp_key(self):
        # 正式版 > 预发布版
        pre = ((1,),) if not self.prerelease else ((0,) + _prekey(self.prerelease),)
        return (self.major, self.minor, self.patch) + pre

    def __eq__(self, other):
        return self._cmp_key() == SemVer.parse(str(other))._cmp_key()

    def __lt__(self, other):
        return self._cmp_key() < SemVer.parse(str(other))._cmp_key()

    def __le__(self, other):
        return self._cmp_key() <= SemVer.parse(str(other))._cmp_key()

    def __gt__(self, other):
        return self._cmp_key() > SemVer.parse(str(other))._cmp_key()

    def __ge__(self, other):
        return self._cmp_key() >= SemVer.parse(str(other))._cmp_key()

    def __str__(self):
        s = "%d.%d.%d" % (self.major, self.minor, self.patch)
        if self.prerelease:
            s += "-" + ".".join(str(p) for p in self.prerelease)
        if self.build:
            s += "+" + self.build
        return s

    def __repr__(self):
        return "SemVer(%r)" % str(self)


def _prekey(items):
    out = []
    for it in items:
        if isinstance(it, int) or it.isdigit():
            out.append((0, int(it)))
        else:
            out.append((1, it))
    return tuple(out)
