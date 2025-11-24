#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_unicode

:Synopsis:

:Author:
    servilla

:Created:
    4/11/24
"""
import emlvp.unicode_inspector as ui


def test_unicode_list(test_data):
    with open(f"{test_data}/eml-2.2.0-unicode.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    unicode_list = ui.unicode_list(xml)
    assert len(unicode_list) == 61
