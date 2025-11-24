#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_dereferencer

:Synopsis:

:Author:
    servilla

:Created:
    1/26/23
"""
from emlvp.dereferencer import Dereferencer


def test_dereference(test_data):
    with open(f"{test_data}/eml-2.2.0-dereference.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    d = Dereferencer(pretty_print=True)
    xml = d.dereference(xml)
    assert xml is not None
