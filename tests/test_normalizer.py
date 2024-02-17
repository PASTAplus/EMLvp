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
import os

import pytest

import tests

from emlvp.normalizer import normalize


@pytest.fixture()
def test_data():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path
    return test_data


def test_dereference(test_data):
    with open(f"{test_data}/eml-2.2.0.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    xml = normalize(xml)
    assert xml is not None
