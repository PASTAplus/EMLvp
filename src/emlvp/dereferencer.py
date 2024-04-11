#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: dereferencer

:Synopsis:

:Author:
    servilla

:Created:
    1/26/23
"""
import copy

import daiquiri
from lxml import etree

from emlvp import exceptions


logger = daiquiri.getLogger(__name__)


class Dereferencer:
    """
    Expands EML XML content by dereferencing "references" element to content defined
    by the "id" attribute of a source element.
    """

    def __init__(self, pretty_print=False):
        """
        Class init method.
        :param pretty_print: Boolean to indicate if dereferenced EML XML is formatted for viewing
        """
        self.pretty_print = pretty_print

    def dereference(self, xml: str) -> str:
        """
        Dereferences an EML XML document instance.
        :param xml: EML XML document instance as a unicode string.
        :return str: Expanded EML XML.
        """

        try:
            xml = xml.encode("utf-8")
        except UnicodeEncodeError as e:
            logger.debug(e)
            raise exceptions.UTF8Error(e)

        root = etree.fromstring(xml)

        references_nodes = root.xpath(".//references")
        for references in references_nodes:
            source_node = root.xpath(f".//*[@id='{references.text.strip()}']")[0]
            source_children = source_node.getchildren()
            parent_node = references.getparent()
            parent_node.remove(references)
            n_children = len(source_children)
            # Add children in reverse to ensure correct order when using E.insert() at position 0
            for child in range(n_children, 0, -1):
                replicant = copy.deepcopy(source_children[child - 1])
                parent_node.insert(0, replicant)

        return etree.tostring(root, pretty_print=self.pretty_print).decode("utf-8")
