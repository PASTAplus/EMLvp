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
import pytest

import emlvp.exceptions as exceptions
from emlvp.validator import Validator


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
    with pytest.raises(exceptions.XMLSyntaxError):
        v.validate(xml)
