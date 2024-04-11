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
import os

import pytest

import tests
import emlvp.unicode_inspector as ui


@pytest.fixture()
def test_data():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path
    return test_data


def test_unicode_list(test_data):
    with open(f"{test_data}/eml-2.2.0-unicode.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    unicode_list = ui.unicode_list(xml)
    assert len(unicode_list) == 61
