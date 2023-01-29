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


logger = daiquiri.getLogger(__name__)


class Dereferencer(object):

    def __init__(self, pretty_print=False):
        self.pretty_print = pretty_print

    def dereference(self, xml: str) -> str:

        xml = xml.encode("utf-8")
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
