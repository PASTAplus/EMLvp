#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    unicode_inspector

:Synopsis:

:Author:
    servilla

:Created:
    4/11/24
"""
import unicodedata


def unicode_list(xml: str) -> list:
    """
    List all unicode characters in the given XML with codepoints greater than ASCII 127
    as a list of tuples: (row, col, char, cp, name)
    :param xml:
    :return list:
    """
    unicodes = []
    n = 0
    lines = xml.split("\n")
    for line in lines:
        n += 1
        for c in range(len(line)):
            i = line[c]
            if ord(i) >= 127:
                row = n
                col = c + 1
                char = i
                cp = ord(i)
                name = unicodedata.name(i, "Unknown")
                unicodes.append((row, col, char, cp, name))

    return unicodes
