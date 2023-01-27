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
from pathlib import Path

import daiquiri
from lxml import etree

import emlvp.exceptions as exceptions


logger = daiquiri.getLogger(__name__)


class Dereferencer(object):

    def __init__(self, pretty_print=False):
        self.pretty_print = pretty_print

    def dereference(self, xml: str) -> str:

        # Accept either file or a string for source of EML XML
        if Path(xml).is_file():
            with open(xml, "r") as f:
                xml = f.read().encode("utf-8")
        else:
            try:
                xml = xml.encode("utf-8")
            except AttributeError as e:
                logger.error(e)

        root = etree.fromstring(xml)

        references_nodes = root.xpath(".//references")
        for references in references_nodes:
            source_node = root.xpath(f".//*[@id='{references.text.strip()}']")[0]
            source_children = source_node.getchildren()
            parent_node = references.getparent()
            parent_node.remove(references)
            for child in source_children:
                replicant = copy.deepcopy(child)
                parent_node.append(replicant)

        return etree.tostring(root, pretty_print=self.pretty_print).decode("utf-8")



