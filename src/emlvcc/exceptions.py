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


class EMLVCCError(Exception):
    pass


class ParseError(EMLVCCError):
    pass


class SaxError(EMLVCCError):
    pass


class SchemaIncludeError(EMLVCCError):
    pass


class ValidationError(EMLVCCError):
    pass


class XPathError(EMLVCCError):
    pass


class XMLSchemaError(EMLVCCError):
    pass


class XMLSchemaParseError(EMLVCCError):
    pass


class XMLSyntaxError(EMLVCCError):
    pass


class XSLTError(EMLVCCError):
    pass
