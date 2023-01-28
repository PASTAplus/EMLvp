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
import daiquiri
from lxml import etree

import emlvp.exceptions as exceptions


logger = daiquiri.getLogger(__name__)


class Validator(object):

    def __init__(self, schema: str):
        self.schema = schema

    def validate(self, xml: str):

        xml = xml.encode("utf-8")

        try:
            doc = etree.fromstring(xml)
            schema = etree.XMLSchema(file=self.schema)
            schema.assertValid(doc)
        except etree.DocumentInvalid as e:
            logger.debug(e)
            raise exceptions.ValidationError(e)
        except etree.ParserError as e:
            logger.debug(e)
            raise exceptions.ValidationError(e)
        except etree.XIncludeError as e:
            logger.debug(e)
            raise exceptions.ValidationError(e)
        except etree.XMLSchemaParseError as e:
            logger.debug(e)
            raise exceptions.ValidationError(e)
        except etree.XMLSyntaxError as e:
            logger.debug(e)
            raise exceptions.ValidationError(e)

