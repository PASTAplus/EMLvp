#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: __init__

:Synopsis:

:Author:
    servilla

:Created:
    1/21/23
"""
import logging
from pathlib import Path
import sys

import daiquiri


cwd = Path(".").resolve().as_posix()
logfile = cwd + "/tests.log"
daiquiri.setup(level=logging.DEBUG,
               outputs=(daiquiri.output.File(logfile), "stdout",))
logger = daiquiri.getLogger(__name__)

sys.path.insert(0, Path("../src").resolve().as_posix())
test_data_path = cwd + "/data"
schema_path = Path("../src/emlvp/schemas").resolve().as_posix()

