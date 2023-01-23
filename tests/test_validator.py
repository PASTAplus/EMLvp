#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_validator

:Synopsis:

:Author:
    servilla

:Created:
    1/21/23
"""
import os

import pytest

import tests

from emlvp.config import Config
import emlvp.exceptions as exceptions
from emlvp.validator import Validator


@pytest.fixture()
def test_data():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path
    return test_data


def test_validate_valid(test_data):
    v = Validator(Config.EML2_2_0_local)
    v.validate(f"{test_data}/eml-2.2.0.xml")


def test_validate_invalid(test_data):
    v = Validator(Config.EML2_2_0_local)
    with pytest.raises(exceptions.ValidationError):
        v.validate(f"{test_data}/eml-2.2.0-invalid.xml")


def test_validate_missing_eml_tag(test_data):
    v = Validator(Config.EML2_2_0_local)
    with pytest.raises(exceptions.ValidationError):
        v.validate(f"{test_data}/eml-2.2.0-missing-eml-tag.xml")


def test_validate_missing_package_id(test_data):
    v = Validator(Config.EML2_2_0_local)
    with pytest.raises(exceptions.ValidationError):
        v.validate(f"{test_data}/eml-2.2.0-missing-package-id.xml")


def test_validate_syntax_error(test_data):
    v = Validator(Config.EML2_2_0_local)
    with pytest.raises(exceptions.XMLSyntaxError):
        v.validate(f"{test_data}/eml-2.2.0-syntax-error.xml")
