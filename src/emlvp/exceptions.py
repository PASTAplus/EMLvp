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


class CircularReferenceIdError(EMLVPError):
    pass


class CustomUnitError(EMLVPError):
    pass


class DuplicateIdError(EMLVPError):
    pass


class InconsistentSystemError(EMLVPError):
    pass


class InspectionError(EMLVPError):
    pass


class MissingAdditionalMetadataDescribesIdError(EMLVPError):
    pass


class MissingAnnotationParentIdError(EMLVPError):
    pass


class MissingAnnotationReferencsIdError(EMLVPError):
    pass


class MissingReferenceIdError(EMLVPError):
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
