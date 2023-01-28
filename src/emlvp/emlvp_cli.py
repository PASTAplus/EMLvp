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
import os
from pathlib import Path
import sys

import click
import daiquiri

from emlvp.config import Config
from emlvp.dereferencer import Dereferencer
from emlvp.exceptions import ValidationError, ParseError
from emlvp.parser import Parser
from emlvp.validator import Validator


cwd = os.path.dirname(os.path.realpath(__file__))
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

    if "https://eml.ecoinformatics.org/eml-2.2.0" in xml:
        schema = Config.EML2_2_0_local
    elif "eml://ecoinformatics.org/eml-2.1.1" in xml:
        schema = Config.EML2_1_1_local
    elif "eml://ecoinformatics.org/eml-2.1.0" in xml:
        schema = Config.EML2_1_0_local
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


help_target = "Either EML XML file or directory containing EML XML file(s)"
help_dereference = "Dereference EML XML file(s) (default is False)"
help_fail_fast = "Exit on first exception encountered (default is False)"
help_pretty_print = "Pretty print output for dereferenced EML XML (default is False)"
verbose_help = "Send output to standard out (-v or -vv or -vvv for increasing output)"


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("target", required=True, nargs=-1)
@click.option("-d", "--dereference", is_flag=True, default=False, help=help_dereference)
@click.option("-f", "--fail-fast", is_flag=True, default=False, help=help_fail_fast)
@click.option("-p", "--pretty-print", is_flag=True, default=False, help=help_pretty_print)
@click.option("-v", "--verbose", count=True, help=verbose_help)
def main(target: tuple, dereference: bool, fail_fast: bool, pretty_print: bool, verbose: int):
    """
        Performs validation of EML XML file(s)\n
            1. XML schema validation\n
            2. EML parsing for references/id resolution\n
            3. Dereference references/id into expanded EML XML and re-validate/parse\n

        \b
            TARGET: EML XML file or directory containing EML XML file(s) (may be repeated)
    """

    for t in target:
        if Path(t).is_file():
            with open(t, "r") as f:
                xml = f.read()
                try:
                    xml = vpd(xml, dereference, fail_fast, pretty_print)
                    if verbose >= 1:
                        print(f"{Path(t).name}\n")
                        if verbose >= 2:
                            print(xml)
                except (ValidationError, ParseError) as e:
                    if verbose >= 0:
                        print(f"{Path(t).name}\n{Style.RED}{e}{Style.RESET}\n")
                        if verbose >= 2:
                            print(xml)
        elif Path(t).is_dir():
            for tf in Path(t).glob("*.xml"):
                with open(tf, "r") as f:
                    xml = f.read()
                    try:
                        xml = vpd(xml, dereference, fail_fast, pretty_print)
                        if verbose >= 1:
                            print(f"{Path(tf).name}\n")
                            if verbose >= 2:
                                print(xml)
                    except (ValidationError, ParseError) as e:
                        if verbose >= 0:
                            print(f"{Path(tf).name}\n{Style.RED}{e}{Style.RESET}\n")
                            if verbose >= 2:
                                print(xml)
        else:
            logger.error(f"Target {t} is not a file or directory")
            sys.exit(1)

    return 0


if __name__ == "__main__":
    main()
