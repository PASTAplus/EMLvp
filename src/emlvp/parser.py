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


def _custom_units(e: etree.Element) -> list:
    custom_units = []
    refs = e.findall(".//{*}customUnit")
    for ref in refs:
        custom_units.append(ref.text.strip())

    return custom_units


class Parser(object):

    def __init__(self, fail_fast: bool = True):
        self.fail_fast = fail_fast
        self.ids = []
        self.references = []
        self.custom_units = []
        self.circular_references = []

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

        self._parse(doc)

        # Varify id uniqueness
        id_duplicates = set([x for x in self.ids if self.ids.count(x) > 1])
        duplicate_id = False
        if len(id_duplicates) > 0:
            duplicate_id = True
            msg_id = f"Duplicate id(s) found: {id_duplicates}"
            logger.error(msg_id)
            if self.fail_fast:
                raise exceptions.DuplicateIdError(msg_id)

        # Varify reference ids exist
        missing_reference_id = False
        for r in self.references:
            references_without_ids = []
            if r not in self.ids:
                references_without_ids.append(r)
                missing_reference_id = True
        if missing_reference_id:
            msg_reference = f"Reference(s) missing Id(s): {self.references}"
            logger.error(msg_reference)
            if self.fail_fast:
                raise exceptions.MissingReferenceIdError(msg_reference)

        # Varify circular reference does not exist
        if len(self.circular_references) > 0:
            msg_circular = f"Circular id/reference(s) exists: {self.circular_references}"
            logger.error(msg_circular)
            if self.fail_fast:
                raise exceptions.CircularReferenceIdError(msg_circular)

        # Varify custom unit definition(s)
        missing_custom_unit_definition = False
        missing_custom_units = []
        for cu in self.custom_units:
            if cu not in self.ids:
                missing_custom_units.append(cu)
                missing_custom_unit_definition = True
        if missing_custom_unit_definition:
            msg_custom_unit = f"Custom unit(s) not defined: {missing_custom_units}"
            logger.error(msg_custom_unit)
            if self.fail_fast:
                raise exceptions.CustomUnitError(msg_custom_unit)

    def _parse(self, e: etree.Element):
        """"Perform single-pass parsing of DOM analyzing each node"""

        has_id = False
        id = None
        for attr in e.attrib:
            if attr == "id":
                has_id = True
                id = e.attrib[attr]
                self.ids.append(id)

        has_reference = False
        reference = None
        for c in e.getchildren():
            if c.tag == "references":
                has_reference = True
                reference = c.text.strip()
                self.references.append(reference)

        if has_id and has_reference:
            self.circular_references.append(f"ID::{id}, REFERENCE::{reference}")

        if e.tag == "customUnit":
            self.custom_units.append(e.text.strip())

        for c in e.getchildren():
            self._parse(c)
