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
import daiquiri
from lxml import etree

from emlvp import exceptions


logger = daiquiri.getLogger(__name__)


class Parser:
    """
    Parses an EML XML document instance inspecting for non-schema related issues. See here for possible
    issues: https://eml.ecoinformatics.org/validation-and-content-references.html
    """

    def __init__(self, fail_fast: bool = False):
        """
        Class init method.
        :param fail_fast: Boolean to indicate whether parsing should fail immediately
        """
        self.fail_fast = fail_fast

    def parse(self, xml: str):
        """
        Parses an EML XML document instance inspecting for non-schema related issues.
        :param xml: EML XML document instance as a unicode string
        :return: None
        :raises emlvp.exceptions.ParseError: Raises ParseError on any invalid content found
        """

        xml = xml.encode("utf-8")
        root = etree.fromstring(xml)

        msg_queue = ""

        # Inspect id attributes in all elements to ensure uniqueness
        id_nodes = root.findall(".//*[@id]")
        ids = [i.attrib["id"] for i in id_nodes]
        id_duplicates = set([id for id in ids if ids.count(id) > 1])
        if len(id_duplicates) > 0:
            msg_duplicate_id = f"Duplicate id(s): {list(id_duplicates)}\n"
            msg_queue += msg_duplicate_id
            logger.debug(msg_duplicate_id)
            if self.fail_fast:
                raise exceptions.ParseError(msg_duplicate_id)

        # Remove duplicates
        ids = set(ids)

        # Inspect references elements for subject ids
        references_nodes = root.findall(".//{*}references")
        references = [r.text.strip() for r in references_nodes]
        missing_reference_id = False
        references_without_ids = []
        for reference in references:
            if reference not in ids:
                references_without_ids.append(reference)
                missing_reference_id = True
        if missing_reference_id:
            msg_reference = f"Missing references id(s): {references_without_ids}\n"
            msg_queue += msg_reference
            logger.debug(msg_reference)
            if self.fail_fast:
                raise exceptions.ParseError(msg_reference)

        # Inspect for circular references (reference parent elements with id attributes)
        has_circular_reference = False
        circular_references = []
        for reference in references_nodes:
            parent = reference.getparent()
            if parent is not None and "id" in parent.attrib:
                circular_references.append(f"{parent.tag}::{reference.text.strip()}")
                has_circular_reference = True
        if has_circular_reference:
            msg_circular_references = f"Circular references: {circular_references}\n"
            msg_queue += msg_circular_references
            logger.debug(msg_circular_references)
            if self.fail_fast:
                raise exceptions.ParseError(msg_circular_references)

        # Inspect for system attribute consistency
        has_system_inconsistency = False
        inconsistent_systems = []
        for reference in references_nodes:
            r_system = None
            if "system" in reference.attrib:
                r_system = reference.attrib["system"]
            for id_node in id_nodes:
                if id_node.attrib["id"] == reference.text.strip():
                    i_system = None
                    if "system" in id_node.attrib:
                        i_system = id_node.attrib["system"]
                    if r_system != i_system:
                        has_system_inconsistency = True
                        inconsistent_systems.append(
                            f"{id_node.tag}::{reference.text.strip()}"
                        )
                    break
        if has_system_inconsistency:
            msg_system_inconsistency = (
                "Inconsistent system attribute(s): {inconsistent_systems}\n"
            )
            msg_queue += msg_system_inconsistency
            logger.debug(msg_system_inconsistency)
            if self.fail_fast:
                raise exceptions.ParseError(msg_system_inconsistency)

        # Inspect custom units for STMML definitions
        has_undefined_custom_unit = False
        missing_custom_unit_ids = []
        custom_unit_nodes = root.findall(".//{*}customUnit")
        custom_units = set([unit.text.strip() for unit in custom_unit_nodes])
        unit_nodes = root.xpath(
            "./additionalMetadata/metadata//*[local-name()='unitList']/*[local-name()='unit'][@id]"
        )
        unit_ids = [unit_id.attrib["id"] for unit_id in unit_nodes]
        for custom_unit in custom_units:
            if custom_unit not in unit_ids:
                has_undefined_custom_unit = True
                missing_custom_unit_ids.append(custom_unit)
        if has_undefined_custom_unit:
            msg_undefined_custom_unit = (
                f"Missing custom unit id(s): {missing_custom_unit_ids}\n"
            )
            msg_queue += msg_undefined_custom_unit
            logger.debug(msg_undefined_custom_unit)
            if self.fail_fast:
                raise exceptions.ParseError(msg_undefined_custom_unit)

        # Inspect parents of annotation elements for subject id (sans the annotations element)
        has_missing_annotation_id = False
        missing_annotation_ids = []
        parents_nodes = root.xpath(
            ".//*[local-name() != 'annotations']/annotation/parent::*"
        )
        for parent in parents_nodes:
            if "id" not in parent.attrib:
                has_missing_annotation_id = True
                missing_annotation_ids.append(parent.tag)
        if has_missing_annotation_id:
            msg_missing_annotation_id = f"Missing subject id for annotation parent(s): {missing_annotation_ids}\n"
            msg_queue += msg_missing_annotation_id
            logger.debug(msg_missing_annotation_id)
            if self.fail_fast:
                raise exceptions.ParseError(msg_missing_annotation_id)

        # Inspect references attribute of annotation(s) for subject id
        has_missing_annotation_references_id = False
        missing_annotation_references_ids = []
        annotation_nodes = root.xpath(".//annotations/annotation[@references]")
        annotation_references = set(
            [reference.attrib["references"] for reference in annotation_nodes]
        )
        for annotation_reference in annotation_references:
            if annotation_reference not in ids:
                has_missing_annotation_references_id = True
                missing_annotation_references_ids.append(annotation_reference)
        if has_missing_annotation_references_id:
            msg_missing_annotation_references = (
                f"Missing subject id for annotation references: {missing_annotation_references_ids}\n"
            )
            msg_queue += msg_missing_annotation_references
            logger.debug(msg_missing_annotation_references)
            if self.fail_fast:
                raise exceptions.ParseError(msg_missing_annotation_references)

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
            msg_missing_describes_id = f"Missing additionalMetadata describes subject id: {missing_describes_ids}\n"
            msg_queue += msg_missing_describes_id
            logger.debug(msg_missing_describes_id)
            if self.fail_fast:
                raise exceptions.ParseError(msg_missing_describes_id)

        # Fail slow
        if len(msg_queue) > 0:
            raise exceptions.ParseError(msg_queue.strip())
