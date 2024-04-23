#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: validator

:Synopsis:

:Author:
    servilla

:Created:
    1/21/23
"""
import os
from pathlib import Path

import daiquiri
from lxml import etree

from emlvp import exceptions


logger = daiquiri.getLogger(__name__)


def schema_path() -> str:
    """
    Return path to installed schemas.
    :return: Path to emlvp installed schemas
    :rtype: str
    """
    return os.path.abspath(os.path.dirname(__file__)) + "/schemas"


class Validator:
    """
    Validates an EML XML document for being well formed and schema syntax correct.
    """

    def __init__(self, schema: str):
        """
        Class init method.
        :param schema: path to root schema eml.xsd
        """
        self.schema = schema
        if not Path(self.schema).is_file():
            msg = f"Cannot locate root schema file: {schema}"
            raise IOError(msg)

    def validate(self, xml: str):
        """
        Validates an EML XML document instance
        :param xml: EML XML document instance as a unicode string
        :return: None
        :raises emlvp.exceptions.ValidationError, emlvp.exceptions.ParseError, emlvp.exceptions.XIncludeError,
            emlvp.exceptions.XMLSchemaParseError, emlvp.exceptions.XMLSyntaxError
        """

        try:
            xml = xml.encode("utf-8")
        except UnicodeEncodeError as e:
            logger.debug(e)
            raise exceptions.UTF8Error(e)

        try:
            doc = etree.fromstring(xml)
            schema = etree.XMLSchema(file=self.schema)
            schema.assertValid(doc)
        except etree.DocumentInvalid as e:
            logger.debug(e)
            raise exceptions.ValidationError(e.error_log)
        except etree.ParserError as e:
            logger.debug(e)
            raise exceptions.ParserError(e)
        except etree.XIncludeError as e:
            logger.debug(e)
            raise exceptions.XIncludeError(e)
        except etree.XMLSchemaParseError as e:
            logger.debug(e)
            raise exceptions.XMLSchemaParseError(e)
        except etree.XMLSyntaxError as e:
            logger.debug(e)
            raise exceptions.XMLSyntaxError(e)


def _parse_validation_errors(e) -> str:
    """
    Parse validation errors into a list of strings
    :param e: ValidationError exception
    :return: List of strings
    """
    errors = ""
    for error in str(e.error_log).split("\n"):
        errors += error + "\n"
    return errors


