#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_normalizer

:Synopsis:

:Author:
    servilla

:Created:
    2/16/24
"""
from emlvp.normalizer import normalize


def test_dereference(test_data):
    with open(f"{test_data}/eml-2.2.0.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    xml = normalize(xml)
    assert xml is not None
