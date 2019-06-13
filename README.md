[![Software License](https://img.shields.io/badge/License-MIT-orange.svg?style=flat-square)](https://github.com/AntoineAugusti/table-schema-to-markdown/blob/master/LICENSE.md)
![CircleCI](https://img.shields.io/circleci/project/github/AntoineAugusti/table-schema-to-markdown.svg?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/table-schema-to-markdown.svg?style=flat-square)
![PyPI Python version](https://img.shields.io/pypi/pyversions/table-schema-to-markdown.svg?style=flat-square)

# Table Schema to Markdown
Create a Markdown documentation file from a [Table Schema file](https://frictionlessdata.io/specs/table-schema/).

The original scripts are coming from [doc-generator](https://git.opendatafrance.net/scdl/doc-generator) for the [Validata](https://validata.fr/) project, which are now available as [an npm package](https://www.npmjs.com/package/@opendataschema/table-schema-to-markdown).

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
```sh
# Print generated Markdown
table-schema-to-md schema.json
# Save to Markdown file
table-schema-to-md schema.json -o documentation.md
```

### In Python
```python
from table_schema_to_markdown import convert_source

# Generate a Markdown documentation from a JSON file
table_schema = '/tmp/schema.json'
with open('/tmp/doc.md', 'a') as out:
    convert_source(table_schema, out)

# Generate Markdown documentation in a string
import io

with io.StringIO() as buff:
    convert_source(table_schema, buff)
    documentation = buff.getvalue()
```

## Generated documentation example
[This table schema file](tests/files/repertoire.json) is rendered in Markdown in [this file](tests/files/expected_repertoire.md).

Find a generated documentation file below.

## Métadonnées d'un répertoire Git

- Auteur : Antoine Augusti <antoine.augusti@example.com>
- Schéma créé le : 12/31/18
- Site web : https://github.com/AntoineAugusti/data-codes-sources-fr
- Clé primaire : `repertoire_url`

### Modèle de données

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|nom|chaîne de caractères|Le nom du répertoire|nom-repertoire|Valeur obligatoire|
|organisation_nom|chaîne de caractères|Le nom de l'organisation|etalab|Valeur obligatoire|
|plateforme|chaîne de caractères|La plateforme de dépôt de code|GitHub|Valeur obligatoire, Valeurs autorisées : GitHub|
|repertoire_url|chaîne de caractères (format `uri`)|L'URL vers le répertoire|https://github.com/etalab/nom-repertoire|Valeur obligatoire|
|description|chaîne de caractères|La description du répertoire|Ce répertoire est utile|Valeur optionnelle|
|est_fork|booléen|Indique si le répertoire est un fork|false|Valeur obligatoire|
|date_creation|date et heure|La date de création du répertoire|2018-12-01T20:00:55Z|Valeur obligatoire|
|derniere_mise_a_jour|date et heure|La date de dernière mise à jour du répertoire|2018-12-01T20:00:55Z|Valeur obligatoire|
|page_accueil|chaîne de caractères|URL vers la page d'accueil du projet|https://etalab.gouv.fr|Valeur optionnelle|
|nombre_stars|nombre entier|Le nombre de fois où le répertoire a été ajouté aux favoris|42|Valeur obligatoire, Valeur minimale : 0|
|nombre_forks|nombre entier|Le nombre de fois où le répertoire a été forké|13|Valeur obligatoire, Valeur minimale : 0|
|licence|chaîne de caractères|La licence du répertoire, telle que détectée par la plateforme|MIT|Valeur optionnelle|
|nombre_issues_ouvertes|nombre entier|Le nombre d'issues actuellement ouvertes|0|Valeur obligatoire, Valeur minimale : 0|
|langage|chaîne de caractères|Le langage principal du répertoire, tel que détecté par la plateforme|Python|Valeur optionnelle|
|topics|chaîne de caractères|Les tags du répertoire|utile,france,opendata|Valeur optionnelle|

## Notice
This software is available under the MIT license.
