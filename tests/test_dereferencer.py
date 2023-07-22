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
import os

import pytest

import tests

import emlvp.exceptions as exceptions
from emlvp.dereferencer import Dereferencer


@pytest.fixture()
def test_data():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path
    return test_data


def test_dereference(test_data):
    with open(f"{test_data}/eml-2.2.0-dereference.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    d = Dereferencer(pretty_print=True)
    xml = d.dereference(xml)
    assert xml is not None




