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

from emlvcc.config import Config
import emlvcc.exceptions as exceptions
import emlvcc.validator as validator


def test_validate():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path

    v = validator.Validator(Config.EML2_2_0_local)

    v.validate(f"{test_data}/eml-2.2.0.xml")

    with pytest.raises(exceptions.ValidationError):
        v.validate(f"{test_data}/eml-2.2.0-invalid.xml")

    with pytest.raises(exceptions.XMLSyntaxError):
        v.validate(f"{test_data}/eml-2.2.0-syntax-error.xml")
