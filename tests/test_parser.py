#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_parser

:Synopsis:

:Author:
    servilla

:Created:
    1/22/23
"""
import os

import pytest

import tests

from emlvp.config import Config
import emlvp.exceptions as exceptions
from emlvp.parser import Parser


def test_parse():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path

    p = Parser()

    p.parse(f"{test_data}/eml-2.2.0.xml")

    with pytest.raises(exceptions.DuplicateIdError):
        p.parse(f"{test_data}/eml-2.2.0-duplicate-ids.xml")

    with pytest.raises(exceptions.MissingReferenceIdError):
        p.parse(f"{test_data}/eml-2.2.0-missing-reference-id.xml")

