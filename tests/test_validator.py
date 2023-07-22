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

import emlvp.exceptions as exceptions
from emlvp.validator import Validator


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


def test_validate_valid(test_data, schema_path):
    with open(f"{test_data}/eml-2.2.0.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    v = Validator(schema_path + "/EML2.2.0/xsd/eml.xsd")
    v.validate(xml)


def test_validate_invalid(test_data, schema_path):
    with open(f"{test_data}/eml-2.2.0-invalid.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    v = Validator(schema_path + "/EML2.2.0/xsd/eml.xsd")
    with pytest.raises(exceptions.ValidationError):
        v.validate(xml)


def test_validate_missing_eml_tag(test_data, schema_path):
    with open(f"{test_data}/eml-2.2.0-missing-eml-tag.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    v = Validator(schema_path + "/EML2.2.0/xsd/eml.xsd")
    with pytest.raises(exceptions.ValidationError):
        v.validate(xml)


def test_validate_missing_package_id(test_data, schema_path):
    with open(f"{test_data}/eml-2.2.0-missing-package-id.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    v = Validator(schema_path + "/EML2.2.0/xsd/eml.xsd")
    with pytest.raises(exceptions.ValidationError):
        v.validate(xml)


def test_validate_syntax_error(test_data, schema_path):
    with open(f"{test_data}/eml-2.2.0-syntax-error.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    v = Validator(schema_path + "/EML2.2.0/xsd/eml.xsd")
    with pytest.raises(exceptions.ValidationError):
        v.validate(xml)
