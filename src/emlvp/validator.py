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
    """
    Validates an EML XML document for being well formed and schema syntax correct.
    """

    def __init__(self, schema: str):
        """
        :param schema: path to root schema eml.xsd
        """
        self.schema = schema

    def validate(self, xml: str):
        """
        Validates an EML XML document instance
        :param xml: EML XML document instance as a unicode string.
        :return: None.
        :exception emlvp.exceptions.ValidationError: Raises ValidationError on any invalid content found.
        """

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

