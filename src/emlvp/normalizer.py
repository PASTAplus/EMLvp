#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    normalizer

:Synopsis:
    Normalize an EML XML document instance, including replacement of non-breaking space characters
    with space characters.

:Author:
    servilla

:Created:
    2/16/24
"""

import daiquiri
from lxml import etree

from emlvp import exceptions


logger = daiquiri.getLogger(__name__)

normalize_whitespace = """<xsl:stylesheet version="1.0"
                       xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       >
           <xsl:output omit-xml-declaration="no" indent="yes"/>
       
           <!-- Template to copy nodes and apply templates to attributes and child nodes -->
           <xsl:template match="@*|node()">
               <xsl:copy>
                   <!-- Apply templates to attributes first to normalize space, then to child nodes -->
                   <xsl:apply-templates select="@*"/>
                   <xsl:apply-templates select="node()"/>
               </xsl:copy>
           </xsl:template>
       
           <!-- Template for normalizing space in text nodes, with specific exclusions -->
           <xsl:template match="text()[not(ancestor::markdown or ancestor::literalLayout or ancestor::objectName or ancestor::attributeName or ancestor::para)]">
               <xsl:value-of select="normalize-space(.)"/>
           </xsl:template>
       
           <!-- Template to normalize space in attribute values -->
           <xsl:template match="@*">
               <!-- Create a new attribute with the same name but normalized value -->
               <xsl:attribute name="{name()}">
                   <xsl:value-of select="normalize-space(.)"/>
               </xsl:attribute>
           </xsl:template>
       </xsl:stylesheet>"""


def normalize(xml: str) -> str:
    """
    Normalize an EML XML document instance
    :param xml: EML XML document instance as a unicode string
    :return: Normalized EML XML document instance as a unicode string
    """
    xslt = etree.XSLT(etree.XML(normalize_whitespace))

    try:
        normalized = str(xslt(etree.XML(xml.replace("\xa0", " ").encode("utf-8"))))
    except UnicodeEncodeError as e:
        logger.debug(e)
        raise exceptions.UTF8Error(e)

    return normalized
