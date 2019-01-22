[![Software License](https://img.shields.io/badge/License-MIT-orange.svg?style=flat-square)](https://github.com/AntoineAugusti/table-schema-to-markdown/blob/master/LICENSE.md)
![CircleCI](https://img.shields.io/circleci/project/github/AntoineAugusti/table-schema-to-markdown.svg?style=flat-square)
![PyPI](https://img.shields.io/pypi/table-schema-to-markdown.svg?style=flat-square)

# Table Schema to Markdown
Create a Markdown documentation file from a [Table Schema file](https://frictionlessdata.io/specs/table-schema/).

The original code is coming from [validata/validata-doc-generator](https://git.opendatafrance.net/validata/validata-doc-generator).

## Installation
```
pip install table-schema-to-markdown
```

## Usage
### Command line tool
The package provides a command line tool.
```
$ table-schema-to-md -h
usage: table-schema-to-md [-h] [-o OUTPUT] [--log LOG] table_schema

positional arguments:
  table_schema          path or URL of table schema file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name
  --log LOG             level of logging messages
```

Example:
```
table-schema-to-md schema.json documentation.md
```

### In Python
```python
from table_schema_to_markdown import convert_source

table_schema = '/tmp/schema.json'
out_file = open('/tmp/doc.md', 'a')

convert_source(table_schema, out_file)
```

## Notice
This software is available under the MIT license.
