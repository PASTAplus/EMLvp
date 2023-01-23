#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: parser

:Synopsis:

:Author:
    servilla

:Created:
    1/22/23
"""
from pathlib import Path

import daiquiri
from lxml import etree

import emlvp.exceptions as exceptions


logger = daiquiri.getLogger(__name__)


def _ids(e: etree.Element) -> list:
    ids = []

    for attr in e.attrib:
        if attr == "id":
            ids.append(e.attrib[attr])

    for c in e.getchildren():
        ids.extend(_ids(c))

    return ids


def _references(e: etree.Element) -> list:
    references = []
    refs = e.findall(".//{*}references")
    for ref in refs:
        references.append(ref.text.strip())

    return references


class Parser(object):

    def __init__(self, fail_fast: bool = True):
        self.fail_fast = fail_fast

    def parse(self, xml: str):
        # Accept either file or a string for source of EML XML
        if Path(xml).is_file():
            with open(xml, "r") as f:
                xml = f.read().encode("utf-8")
        else:
            try:
                xml = xml.encode("utf-8")
            except AttributeError as e:
                logger.error(e)

        doc = etree.fromstring(xml)

        ids = _ids(doc)
        references = _references(doc)

        # Varify id uniqueness
        id_duplicates = set([x for x in ids if ids.count(x) > 1])
        duplicate_id = False
        if len(id_duplicates) > 0:
            duplicate_id = True
            msg_id = f"Duplicate id(s) found: {id_duplicates}"
            logger.error(msg_id)
            if self.fail_fast:
                raise exceptions.DuplicateIdError(msg_id)

        # Varify reference ids exist
        missing_reference_id = False
        for r in references:
            references_without_ids = []
            if r not in ids:
                references_without_ids.append(r)
                missing_reference_id = True
        if missing_reference_id:
            msg_reference = f"Reference(s) missing Id(s): {references}"
            logger.error(msg_reference)
            if self.fail_fast:
                raise exceptions.MissingReferenceIdError(msg_reference)

