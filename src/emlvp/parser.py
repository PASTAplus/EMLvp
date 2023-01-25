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




class Parser(object):

    def __init__(self, fail_fast: bool = True):
        self.fail_fast = fail_fast
        self.id_nodes = None
        self.doc_id_nodes = None
        self.references_nodes = None
        self.custom_unit_nodes = None
        self.stmml_unit_nodes = None

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

        root = etree.fromstring(xml)

        # Inspect id attributes in all elements to ensure uniqueness
        self.id_nodes = root.findall(".//*[@id]")
        ids = [i.attrib["id"] for i in self.id_nodes]
        id_duplicates = set([x for x in ids if ids.count(x) > 1])
        duplicate_id = False
        if len(id_duplicates) > 0:
            duplicate_id = True
            msg_id = f"Duplicate id(s) exist: {list(id_duplicates)}"
            logger.error(msg_id)
            if self.fail_fast:
                raise exceptions.DuplicateIdError(msg_id)

        # Inspect references elements for associated ids (sans additional metadata)
        self.references_nodes = root.findall(".//{*}references")
        self.doc_id_nodes = set(self.id_nodes) - (
                set(root.findall(".//additionalMetadata[@id]")) | set(root.findall(".//additionalMetadata//*[@id]")))
        doc_ids = [i.attrib["id"] for i in self.doc_id_nodes]
        references = [r.text.strip() for r in self.references_nodes]
        missing_reference_id = False
        references_without_ids = []
        for r in references:
            if r not in doc_ids:
                references_without_ids.append(r)
                missing_reference_id = True
        if missing_reference_id:
            msg_reference = f"Missing references id(s) exist: {references_without_ids}"
            logger.error(msg_reference)
            if self.fail_fast:
                raise exceptions.MissingReferenceIdError(msg_reference)

        # Inspect for circular references
        has_circular_reference = False
        circular_references = []
        for r in self.references_nodes:
            p = r.getparent()
            if p is not None and "id" in p.attrib:
                circular_references.append(f"{p.tag}::{r.text.strip()}")
                has_circular_reference = True
        if has_circular_reference:
            msg_circular = f"Circular references exist: {circular_references}"
            logger.error(msg_circular)
            if self.fail_fast:
                raise exceptions.CircularReferenceIdError(msg_circular)

        # Inspect for system attribute consistency
        has_system_inconsistency = False
        inconsistent_systems = []
        for r in self.references_nodes:
            r_system = None
            if "system" in r.attrib:
                r_system = r.attrib["system"]
            for i in self.id_nodes:
                if i.attrib["id"] == r.text.strip():
                    i_system = None
                    if "system" in i.attrib:
                        i_system = i.attrib["system"]
                    if r_system != i_system:
                        has_system_inconsistency = True
                        inconsistent_systems.append(f"{i.tag}::{r.text.strip()}")
                    break
        if has_system_inconsistency:
            msg_system_inconsistency = "Inconsistent system attribute(s) exist: {inconsistent_systems}"
            logger.error(msg_system_inconsistency)
            if self.fail_fast:
                raise exceptions.InconsistentSystemError(msg_system_inconsistency)

        # Inspect custom units for STMML definitions
        has_undefined_custom_unit = False
        undefined_custom_units = []
        self.custom_unit_nodes = root.findall(".//{*}customUnit")
        custom_units = set([u.text.strip() for u in self.custom_unit_nodes])
        self.stmml_unit_nodes = root.findall("./additionalMetadata//{*}unit[@id]")
        unit_ids = [i.attrib["id"] for i in self.stmml_unit_nodes]
        for custom_unit in custom_units:
            if custom_unit not in unit_ids:
                has_undefined_custom_unit = True
                undefined_custom_units.append(custom_unit)
        if has_undefined_custom_unit:
            msg_undefined_custom_unit = f"Undefined custom unit(s) exist: {undefined_custom_units}"
            logger.error(msg_undefined_custom_unit)
            if self.fail_fast:
                raise exceptions.CustomUnitError(msg_undefined_custom_unit)
