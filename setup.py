#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: setup.py

:Synopsis:

:Author:
    servilla

:Created:
    2023-01-21
"""
from os import path
from setuptools import find_packages, setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "LICENSE"), encoding="utf-8") as f:
    full_license = f.read()

with open(path.join(here, "./src/emlvp/VERSION.txt"), encoding="utf-8") as f:
    version = f.read()


setup(
    name='emlvp',
    version=version,
    description='EMLvp (validator and parser)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mark Servilla",
    url="https://github.com/servilla/EMLvp",
    license=full_license,
    packages=find_packages(where="src", include=["emlvp"]),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=" >= 3.10",
    install_requires=["lxml>=4.9.2", "click>=8.1.3", "daiquiri>=3.0.0"],
    entry_points={"console_scripts": ["emlvp=emlvp.emlvp_cli:main"]},
    classifiers=["License :: OSI Approved :: Apache Software License",],
)


def main():
    return 0


if __name__ == "__main__":
    main()
