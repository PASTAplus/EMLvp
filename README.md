# EMLvp (validator and parser)

![EMLvp](https://github.com/PASTAplus/EMLvp/actions/workflows/python-package-conda.yml/badge.svg) ![RTD](https://readthedocs.org/projects/emlvp/badge/?version=latest)

See [this documentation](https://emlvp.readthedocs.io/en/latest/) on "Read the Docs".

## Introduction

**EMLvp** is a Python 3 library to validate and parse Ecological Metadata
Language XML documents for compliance with the EML metadata standard,
including XML schema validation and ensuring that references resolve to
existing ids. See the [EML normative documentation](https://eml.ecoinformatics.org/validation-and-content-references.html)
for reference.

The **EMLvp** package is both a command line interface (CLI) application that
can be used in a local environment and an EML validation and parsing API that
may be imported into other Python modules. The CLI application, `emlvp`, is
also used as a reference implementation for the emlvp API. The EMLvp package
API provides three object classes that 1) perform XML schema validation -
`Validator`, 2) EML compliance parsing - `Parser`, and 3) dereference EML
`<references>` elements into their normalized structures  - `Derefencer`.

Compliance includes the following inspections:
 1.  `id` attributes in all elements are unique,
 2.  `references` elements for subject `id`,
 3.  for circular `references` (`references` parent elements with `id` attributes),
 4.  for `system` attribute consistency,
 5.  `customUnit` for STMML definitions,
 6.  parents of `annotation` elements for subject `id` (sans the annotations element),
 7.  `references` attribute of annotation(s) for subject id, and
 8.  `additionalMetadata` `describes` attribute for subject id.

The `emlvp` application accepts an Ecological Metadata Language XML document
file as input or a directory containing EML XML document files with a “.xml”
file extension. Once an EML XML document is identified, the application will
immediately perform a schema validation inspection followed by EML compliance
parsing that verifies the document is compliant with rules that go beyond what
is possible with XML schema validation (see above). In addition, the `emlvp`
application can normalize the EML XML document by removing insignificant white
space, including replacing non-breaking spaces with regular spaces.


## Installation

**EMLvp** may be install using pip: `pip install emlvp`. You may also install from GitHub by cloning the repository
and then using pip to install **EMLvp** with `setup.py`. The `emlvp` command line application is installed as part
of the pip installation, as are the XML schema files for EML 2.1.0, 2.1.1, and 2.2.0. **EMPvp** is dependent on the
following Python packages: `Python` >= 3.10, `lxml` >= 4.9.2, `click` >= 8.1.3, and `daiquiri` >= 3.0.0.

## Quickstart Guide

**EMLvp** can be used directly on the command line with the `emlvp` application or embedded into another Python
project. Its purpose is to inspect and analyze an EML XML metadata document to ensure it complies with both schema and
non-schema requirements. `emlvp` simply follows a three step analysis:

 1. Perform schema validation.
 2. Parse and inspect the document for non-schema requirements (above).
 3. If requested, dereference the "references/ids" of the EML and repeat steps 1 and 2.

If at any point during the analysis an error occurs, `emlvp` will either report the error and exit immediately
(fail-fast) or continue to analyze the document and collect all additional errors until the end of the analysis,
at which time the errors are reported (fail-slow). The `emlvp` help provides the following description:

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
  -l, --list_unicode  List non-ASCII unicode characters, along with unicode
                      data
  -n, --normalize     Normalize EML XML file(s) before parsing and validating
                      (default is False).
  -p, --pretty-print  Pretty print output for dereferenced EML XML (default is
                      False).
  -s, --statistics    Show post processing inspection statistics.
  -u, --unicode       Highlight non-ASCII unicode characters in EML output
                      (-uu for line numbers)
  -v, --verbose       Send output to standard out (-v or -vv or -vvv for
                      increasing output).
  --version           Output emlvp version and exit.
  -h, --help          Show this message and exit.
```

As noted above, the "TARGET" argument may be one or more space separate EML XML files or a directory containing many
EML XML files (these files must end with the ".xml" extension). For example:

```
 > emlvp edi.1252.1.xml
 edi.1252.1.xml
 Missing custom unit id(s): ['total abundance', 'logarithmic']
```

If no errors are found, `emlvp` ends quietly and with no fanfare.

To use **EMLvp** in your own Python project, you would need to "import" the necessary class module and perform the
appropriate analysis against the EML XML document. For example::

```Python
 >>> import emlvp.validator as validator
 >>> from emlvp.validator import Validator
 >>>
 >>> with open("edi.1252.1.xml", "r") as f:
 ...     xml = f.read()
 ...
 >>> schema_path = validator.schema_path()
 >>> v = Validator(schema_path + "/EML2.2.0/xsd/eml.xsd")
 >>> v.validate(xml)
 >>>
 >>> from emlvp.parser import Parser
 >>> p = Parser()
 >>> p.parse(xml)
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
   File "/home/user/anaconda3/envs/emlvp/lib/python3.10/site-packages/emlvp/parser.py", line 185, in parse
     raise exceptions.ParseError(msg_queue.strip())
 emlvp.exceptions.ParseError: Missing custom unit id(s): ['logarithmic', 'total abundance']
 >>>
```

Applications that use the API should rely on exceptions to indicate an error has occurred in either validation or
parsing of the EML XML document.

## EMLvp Class API

### validator:

```Python
class Validator(object):
  """
  Validates an EML XML document for being well formed and schema syntax correct.
  """

def __init__(self, schema: str):
  """
  Class init method.
  :param schema: path to root schema eml.xsd
  """

def validate(self, xml: str):
  """
  Validates an EML XML document instance
  :param xml: EML XML document instance as a unicode string
  :return: None
  :raises emlvp.exceptions.ValidationError, emlvp.exceptions.ParseError, emlvp.exceptions.XIncludeError,
    emlvp.exceptions.XMLSchemaParseError, emlvp.exceptions.XMLSyntaxError
  """
```

### parser:

```Python
class Parser(object):
   """
   Parses an EML XML document instance inspecting for non-schema related issues. See here for possible
   issues: https://eml.ecoinformatics.org/validation-and-content-references.html
   """

def __init__(self, fail_fast: bool = False):
   """
   Class init method.
   :param fail_fast: Boolean to indicate whether parsing should fail immediately
   """

def parse(self, xml: str):
   """
   Parses an EML XML document instance inspecting for non-schema related issues.
   :param xml: EML XML document instance as a unicode string
   :return: None
   :raises emlvp.exceptions.ParseError: Raises ParseError on any invalid content found
   """
```

### derferencer:

```Python
class Dereferencer(object):
   """
   Expands EML XML content by dereferencing "references" element to content defined
   by the "id" attribute of a source element.
   """

def __init__(self, pretty_print=False):
   """
   Class init method.
   :param pretty_print: Boolean to indicate if dereferenced EML XML is formatted for viewing
   """

def dereference(self, xml: str) -> str:
   """
   Dereferences an EML XML document instance.
   :param xml: EML XML document instance as a unicode string.
   :return str: Expanded EML XML.
   """
```

## EMLvp Helper Function API

### normalizer

```Python
def normalize(xml: str) -> str:
   """
   Normalize an EML XML document instance
   :param xml: EML XML document instance as a unicode string
   :return: Normalized EML XML document instance as a unicode string
   """
```

### unicode_inspector

```Python
def unicode_list(xml: str) -> list:
    """
    List all unicode characters in the given XML with codepoints greater than ASCII 127
    as a list of tuples: (row, col, char, cp, name)
    :param xml:
    :return list:
    """
```