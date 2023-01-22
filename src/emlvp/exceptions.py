#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: exceptions

:Synopsis:

:Author:
    servilla

:Created:
    1/21/23
"""
import daiquiri


logger = daiquiri.getLogger(__name__)


class EMLVPError(Exception):
    pass


class ParseError(EMLVPError):
    pass


class SaxError(EMLVPError):
    pass


class SchemaIncludeError(EMLVPError):
    pass


class ValidationError(EMLVPError):
    pass


class XPathError(EMLVPError):
    pass


class XMLSchemaError(EMLVPError):
    pass


class XMLSchemaParseError(EMLVPError):
    pass


class XMLSyntaxError(EMLVPError):
    pass


class XSLTError(EMLVPError):
    pass
