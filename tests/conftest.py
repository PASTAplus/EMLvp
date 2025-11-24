#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    conftest.py

:Synopsis:

:Author:
    servilla

:Created:
    11/23/25
"""
import os

import pytest

import tests


@pytest.fixture()
def test_data():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path
    return test_data


@pytest.fixture()
def schema_path():
    if "SCHEMA_PATH" in os.environ:
        schema_path = os.environ["SCHEMA_PATH"]
    else:
        schema_path = tests.schema_path
    return schema_path
