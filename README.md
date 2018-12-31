# Table Schema to Markdown
Crée un fichier de documentation Markdown à partir d'un [fichier Table Schema](https://frictionlessdata.io/specs/table-schema/).

Le code de base provient de [validata/validata-doc-generator](https://git.opendatafrance.net/validata/validata-doc-generator).

## Utilisation
Requiert l'utilisation de Python 3.

```sh
python main.py --help

usage: main.py [-h] [-o OUTPUT] [--log LOG] table_schema

positional arguments:
  table_schema          path or URL of table schema file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name
  --log LOG             level of logging messages
```

Vers la sortie standard :
```
python main.py schema.json
```

Vers un fichier:
```
python main.py schema.json -o doc.md
```
