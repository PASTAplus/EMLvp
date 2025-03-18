# EMLvp change log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## (1.2.6) 2025-03-17
### Changed/Fixed
- Remove pip dependency from pyproject.toml
- Update dependencies in pyproject.toml

## (1.2.5) 2025-03-17
### Changed/Fixed
- Revert Python dependency from >=3.12 to >=3.11

## (1.2.4) 2025-03-15
### Changed/Fixed
- Refactor ValidationException output processing to handle multiple errors

## (1.2.3) 2025-03-14
### Changed/Fixed
- Fix crash when error_log attribute splits error messages across multiple list elements

## (1.2.2) 2024-06-06
### Changed/Fixed
- Fix normalize xslt to replace "markdup" with "markdown"

## (1.2.1) 2024-05-05
### Changed/Fixed
- Set default value as "Unknown" for unicodedata.name function

## (1.2.0) 2024-04-22
### Changed/Fixed
- Update for validation exception list instead of single first error

## (1.1.0) 2024-02-17
### Changed/Fixed
- Catch ValueError in `process_one_document`
- Add unicode inspections to EML documents

## (1.0.0) 2024-02-17
### Changed/Fixed
- Add option to normalize whitespace in EML XML documents
- Release version 1.0.0 - woohoo!

## (0.0.6) 2023-07-21
### Changed/Fixed
- Force opening all files as UTF-8 to support Windows
- Fix scope of summary statistics output

## (0.0.5) 2023-02-06
### Changed/Fixed
- Apply "black" formatting and "pylint" refactors

## (0.0.4) 2023-02-02
### Changed/Fixed
- Add version option to emlvp CLI application

## (0.0.3) 2023-02-02
### Changed/Fixed
- Update documentation

## (0.0.2) 2023-02-01
### Changed/Fixed
- Add explicit dependencies to setup.py

## (0.0.1) 2023-01-31
### Changed/Fixed
- First release
