# EMLvp (Ecological Metadata Language validator and parser)

![EMLvp](https://github.com/PASTAplus/EMLvp/actions/workflows/python-package-conda.yml/badge.svg) ![RTD](https://readthedocs.org/projects/emlvp/badge/?version=latest)

A Python 3 library to validate and parse Ecological Metadata Lanaguage XML documents for compliance (see the
official EML documentation for reference: https://eml.ecoinformatics.org/validation-and-content-references.html)

The **EMLvp** package is both a command line interface (CLI) application that can be used in a local environment and an
EML validation and parsing API that may be imported into other Python modules. The CLI application, `emlvp`, is also
used as a reference implementation for the emlvp API. The EMLvp package API provides three object classes that 1)
perform XML schema validation - `Validator`, 2) EML compliance parsing - `Parser`, and 3) dereference EML 
`<references>` elements into their normalized structures  - `Derefencer`. (see 
  [here](https://emlvp.readthedocs.io/en/latest/) for details)

Compliance includes the following inspections:
 1.  `id` attributes in all elements are unique,
 2.  `references` elements for subject `id`,
 3.  for circular `references` (`references` parent elements with `id` attributes),
 4.  for `system` attribute consistency,
 5.  `customUnit` for STMML definitions,
 6.  parents of `annotation` elements for subject `id` (sans the annotations element),
 7.  `references` attribute of annotation(s) for subject id, and
 8.  `additionalMetadata` `describes` attribute for subject id.

The `emlvp` application accepts an Ecological Metadata Language XML document file as input or a directory containing
EML XML document files with a “.xml” file extension. Once an EML XML document is identified, the application will
immediately perform a schema (and other) validation inspection followed by EML compliance parsing that inspects the
document for compliance beyond what is possible with XML schema validation (see
[EML normative documents](https://eml.ecoinformatics.org/validation-and-content-references.html) for details).

```
Usage: emlvp [OPTIONS] TARGET...

  Performs validation of EML XML file(s)

      1. XML schema validation
      2. EML parsing for references/id resolution
      3. Dereference references/id into expanded EML XML and re-validate/parse

      TARGET: EML XML file or directory containing EML XML file(s) (may be repeated)

Options:
  -d, --dereference   Dereference EML XML file(s) (default is False).
  -f, --fail-fast     Exit on first exception encountered (default is False).
  -p, --pretty-print  Pretty print output for dereferenced EML XML (default is
                      False).
  -s, --statistics    Show post processing inspection statistics.
  -v, --verbose       Send output to standard out (-v or -vv or -vvv for
                      increasing output).
  -h, --help          Show this message and exit.
```
