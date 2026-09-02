# -*- coding: utf-8 -*-
import pytest

from agentpassport.semver import SemVer


def test_parse_full():
    v = SemVer.parse("1.2.3")
    assert (v.major, v.minor, v.patch) == (1, 2, 3)


def test_parse_shorthand():
    assert str(SemVer.parse("1")) == "1.0.0"
    assert str(SemVer.parse("1.2")) == "1.2.0"


def test_compare():
    assert SemVer.parse("1.0.0") < SemVer.parse("2.0.0")
    assert SemVer.parse("1.0.0") == SemVer.parse("v1.0.0")


def test_prerelease_ordering():
    # 正式版 > 预发布版
    assert SemVer.parse("1.0.0") > SemVer.parse("1.0.0-beta")
