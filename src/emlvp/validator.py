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
from pathlib import Path

import daiquiri
from lxml import etree

import emlvp.exceptions as exceptions


logger = daiquiri.getLogger(__name__)


class Validator(object):

    def __init__(self, schema: str):
        self.schema = schema

    def validate(self, xml: str):

        # Accept either file or a string for source of EML XML
        if Path(xml).is_file():
            with open(xml, "r") as f:
                xml = f.read().encode("utf-8")
        else:
            try:
                xml = xml.encode("utf-8")
            except AttributeError as e:
                logger.error(e)

        try:
            doc = etree.fromstring(xml)
            schema = etree.XMLSchema(file=self.schema)
            schema.assertValid(doc)
        except etree.DocumentInvalid as e:
            logger.error(e)
            raise exceptions.ValidationError(e)
        except etree.ParserError as e:
            logger.error(e)
            raise exceptions.ParseError(e)
        except etree.XIncludeError as e:
            logger.error(e)
            raise exceptions.SchemaIncludeError(e)
        except etree.XMLSchemaParseError as e:
            logger.error(e)
            raise exceptions.XMLSchemaParseError(e)
        except etree.XMLSyntaxError as e:
            logger.error(e)
            raise exceptions.XMLSyntaxError(e)

