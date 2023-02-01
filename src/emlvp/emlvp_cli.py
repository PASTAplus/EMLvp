#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: emlvp_cli

:Synopsis:

:Author:
    servilla

:Created:
    1/27/23
"""
import logging
from pathlib import Path
import sys

import click
import daiquiri

from emlvp.dereferencer import Dereferencer
from emlvp.exceptions import EMLVPError, ValidationError, ParseError
from emlvp.parser import Parser
from emlvp.validator import Validator


cwd = Path(".").resolve().as_posix()
logfile = cwd + "/emlvp.log"
daiquiri.setup(level=logging.INFO,
               outputs=(daiquiri.output.File(logfile), "stdout",))
logger = daiquiri.getLogger(__name__)


class Style(object):
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    RESET = '\033[0m'


def vpd(xml: str, dereference: bool, fail_fast: bool, pretty_print: bool) -> str:
    """
    Validate, parse, and dereference EML XML file(s)
    :param xml:
    :param dereference:
    :param fail_fast:
    :param pretty_print:
    :return: None
    """

    p = Path(__file__).resolve().parent.as_posix()

    if "https://eml.ecoinformatics.org/eml-2.2.0" in xml:
        schema = p + "/schemas/EML2.2.0/xsd/eml.xsd"
    elif "eml://ecoinformatics.org/eml-2.1.1" in xml:
        schema = p + "/schemas/EML2.1.1/eml.xsd"
    elif "eml://ecoinformatics.org/eml-2.1.0" in xml:
        schema = p + "/schemas/EML2.1.0/eml.xsd"
    else:
        raise ValueError("Cannot determine schema")

    v = Validator(schema)
    v.validate(xml)
    p = Parser(fail_fast=fail_fast)
    p.parse(xml)
    if dereference:
        d = Dereferencer(pretty_print=pretty_print)
        xml = d.dereference(xml)
        v.validate(xml)
        p.parse(xml)

    return xml


def process_one_document(doc: str, dereference: bool, fail_fast: bool, pretty_print: bool, verbose: int):
    with open(doc, "r") as f:
        xml = f.read()
        try:
            xml = vpd(xml, dereference, fail_fast, pretty_print)
            if verbose >= 1:
                print(f"{doc}\n")
                if verbose >= 2:
                    print(xml)
        except (ValidationError, ParseError) as e:
            if verbose >= 0:
                print(f"{doc}\n{Style.RED}{e}{Style.RESET}\n")
                if verbose >= 2:
                    print(xml)
            raise EMLVPError(e)
    pass


help_target = "Either EML XML file or directory containing EML XML file(s)."
help_dereference = "Dereference EML XML file(s) (default is False)."
help_fail_fast = "Exit on first exception encountered (default is False)."
help_pretty_print = "Pretty print output for dereferenced EML XML (default is False)."
help_statistics = "Show post processing inspection statistics."
verbose_help = "Send output to standard out (-v or -vv or -vvv for increasing output)."


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("target", required=True, nargs=-1)
@click.option("-d", "--dereference", is_flag=True, default=False, help=help_dereference)
@click.option("-f", "--fail-fast", is_flag=True, default=False, help=help_fail_fast)
@click.option("-p", "--pretty-print", is_flag=True, default=False, help=help_pretty_print)
@click.option("-s", "--statistics", is_flag=True, default=False, help=help_statistics)
@click.option("-v", "--verbose", count=True, help=verbose_help)
def main(target: tuple, dereference: bool, fail_fast: bool, pretty_print: bool, statistics: bool, verbose: int):
    """
        Performs validation of EML XML file(s)\n
            1. XML schema validation\n
            2. EML parsing for references/id resolution\n
            3. Dereference references/id into expanded EML XML and re-validate/parse\n

        \b
            TARGET: EML XML file or directory containing EML XML file(s) (may be repeated)
    """
    docs_processed = 0
    docs_with_exceptions = 0

    for t in target:
        if Path(t).is_file():
            try:
                docs_processed += 1
                process_one_document(doc=t, dereference=dereference, fail_fast=fail_fast,
                                     pretty_print=pretty_print, verbose=verbose)
            except EMLVPError:
                docs_with_exceptions += 1
        elif Path(t).is_dir():
            for tf in Path(t).glob("*.xml"):
                try:
                    docs_processed += 1
                    process_one_document(doc=str(tf), dereference=dereference, fail_fast=fail_fast,
                                         pretty_print=pretty_print, verbose=verbose)
                except EMLVPError:
                    docs_with_exceptions += 1
        else:
            logger.error(f"Target {t} is not a file or directory")
            sys.exit(1)

        if statistics:
            print(f"Total documents validated: {docs_processed}")
            print(f"Documents that failed validation: {docs_with_exceptions}")

    return 0


if __name__ == "__main__":
    main()
