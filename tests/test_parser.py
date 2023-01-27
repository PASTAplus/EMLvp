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


@pytest.fixture()
def test_data():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path
    return test_data


def test_parse_valid(test_data):
    p = Parser()
    p.parse(f"{test_data}/eml-2.2.0.xml")


def test_parse_duplicate_id(test_data):
    p = Parser()
    with pytest.raises(exceptions.DuplicateIdError):
        p.parse(f"{test_data}/eml-2.2.0-duplicate-id.xml")


def test_parse_missing_additional_metadata_describes_id(test_data):
    p = Parser()
    with pytest.raises(exceptions.MissingAdditionalMetadataDescribesIdError):
        p.parse(f"{test_data}/eml-2.2.0-missing-describes-id.xml")


def test_parse_missing_annotation_parent_id(test_data):
    p = Parser()
    with pytest.raises(exceptions.MissingAnnotationParentIdError):
        p.parse(f"{test_data}/eml-2.2.0-missing-annotation-parent-id.xml")


def test_parse_missing_annotation_references_id(test_data):
    p = Parser()
    with pytest.raises(exceptions.MissingAnnotationReferencsIdError):
        p.parse(f"{test_data}/eml-2.2.0-missing-annotation-references-id.xml")


def test_parse_missing_reference_id(test_data):
    p = Parser()
    with pytest.raises(exceptions.MissingReferenceIdError):
        p.parse(f"{test_data}/eml-2.2.0-missing-reference-id.xml")


def test_parse_circular_reference(test_data):
    p = Parser()
    with pytest.raises(exceptions.CircularReferenceIdError):
        p.parse(f"{test_data}/eml-2.2.0-circular-reference.xml")


def test_parse_missing_custom_unit(test_data):
    p = Parser()
    with pytest.raises(exceptions.CustomUnitError):
        p.parse(f"{test_data}/eml-2.2.0-missing-custom-unit-id.xml")


def test_parse_system_inconsistency(test_data):
    p = Parser()
    with pytest.raises(exceptions.InconsistentSystemError):
        p.parse(f"{test_data}/eml-2.2.0-system-inconsistency.xml")
