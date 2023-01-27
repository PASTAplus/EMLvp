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
        id_nodes = root.findall(".//*[@id]")
        ids = [i.attrib["id"] for i in id_nodes]
        id_duplicates = set([x for x in ids if ids.count(x) > 1])
        duplicate_id = False
        if len(id_duplicates) > 0:
            duplicate_id = True
            msg_id = f"Duplicate id(s) exist: {list(id_duplicates)}"
            logger.error(msg_id)
            if self.fail_fast:
                raise exceptions.DuplicateIdError(msg_id)

        # Inspect references elements for subject ids
        references_nodes = root.findall(".//{*}references")
        references = [r.text.strip() for r in references_nodes]
        missing_reference_id = False
        references_without_ids = []
        for r in references:
            if r not in ids:
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
        for r in references_nodes:
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
        for r in references_nodes:
            r_system = None
            if "system" in r.attrib:
                r_system = r.attrib["system"]
            for i in id_nodes:
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
        missing_custom_unit_ids = []
        custom_unit_nodes = root.findall(".//{*}customUnit")
        custom_units = set([u.text.strip() for u in custom_unit_nodes])
        stmml_unit_nodes = root.findall("./additionalMetadata/metadata/unitList/unit[@id]")
        unit_ids = [i.attrib["id"] for i in stmml_unit_nodes]
        for custom_unit in custom_units:
            if custom_unit not in unit_ids:
                has_undefined_custom_unit = True
                missing_custom_unit_ids.append(custom_unit)
        if has_undefined_custom_unit:
            msg_undefined_custom_unit = f"Missing custom unit id(s) exist: {missing_custom_unit_ids}"
            logger.error(msg_undefined_custom_unit)
            if self.fail_fast:
                raise exceptions.CustomUnitError(msg_undefined_custom_unit)

        # Inspect parents of annotation elements for subject id (sans annotations)
        has_missing_annotation_id = False
        missing_annotation_ids = []
        parents_nodes = root.xpath(".//*[local-name() != 'annotations']/annotation/parent::*")
        for p in parents_nodes:
            if "id" not in p.attrib:
                has_missing_annotation_id = True
                missing_annotation_ids.append(p.tag)
        if has_missing_annotation_id:
            msg_missing_annotation_id = f"Missing subject id for annotation parent(s) exist: {missing_annotation_ids}"
            logger.error(msg_missing_annotation_id)
            if self.fail_fast:
                raise exceptions.MissingAnnotationParentIdError(msg_missing_annotation_id)

        # Inspect references attribute of annotation(s) for subject id
        has_missing_annotation_references_id = False
        missing_annotation_references_ids = []
        annotation_nodes = root.xpath(".//annotations/annotation[@references]")
        annotation_references = set([r.attrib["references"] for r in annotation_nodes])
        for annotation_reference in annotation_references:
            if annotation_reference not in ids:
                has_missing_annotation_references_id = True
                missing_annotation_references_ids.append(annotation_reference)
        if has_missing_annotation_references_id:
            msg_missing_annotation_references = f"Missing subject id for annotation references exist: {missing_annotation_references_ids}"
            logger.error(msg_missing_annotation_references)
            if self.fail_fast:
                raise exceptions.MissingAnnotationReferencsIdError(msg_missing_annotation_references)

        # Inspect additionalMetadata describes for subject id
        has_missing_describes_id = False
        missing_describes_ids = []
        describes_nodes = root.xpath(".//additionalMetadata/describes")
        describes = set([d.text.strip() for d in describes_nodes])
        for describe in describes:
            if describe not in ids:
                has_missing_describes_id = True
                missing_describes_ids.append(describe)
        if has_missing_describes_id:
            msg_missing_describes_id = f"Missing additionalMetadata describes subject id exists: {missing_describes_ids}"
            logger.error(msg_missing_describes_id)
            if self.fail_fast:
                raise exceptions.MissingAdditionalMetadataDescribesIdError(msg_missing_describes_id)