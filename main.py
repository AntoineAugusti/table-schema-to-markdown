#!/usr/bin/env python3
import argparse
import io
import json
import logging
import sys

from collections import OrderedDict
from datetime import datetime

log = logging.getLogger(__name__)

SCHEMA_PROP_MAP = {
    'author': 'Auteur',
    'contributor': 'Contributeurs',
    'version': 'Version',
    'created': 'Schéma créé le',
    'homepage': 'Site web',
    'example': 'Données d\'exemple',
}


TYPE_MAP = {
    'array': 'liste',
    'boolean': 'booléen',
    'date': 'date',
    'datetime': 'date et heure',
    'duration': 'durée',
    'geojson': 'GéoJSON',
    'geopoint': 'point géographique',
    'integer': 'nombre entier',
    'number': 'nombre réel',
    'object': 'objet',
    'string': 'chaîne de caractères',
    'time': 'heure',
    'year': 'année',
    'year-month': 'année et mois',
}

FORMAT_MAP = {
    'email': 'adresse de courriel',
    'uri': 'adresse URL',
    'binary': 'données binaires encodées en base64',
    'uuid': 'identifiant UUID',
}

TYPE_SPECIFIC_MAP = OrderedDict([
    ('decimalChar', 'Séparateur décimal («.» par défaut)'),
    ('groupChar', 'Séparateur de groupes de chiffres («,» par défaut)'),
    # 'bareNumber' : 'Nombre nu', => Needs a specific treatment
    ('trueValues', 'Valeurs considérées comme vraies'),
    ('falseValues', 'Valeurs considérées comme fausses'),
])

CONSTRAINTS_MAP = OrderedDict([
    ('minLength', lambda v: 'Taille minimale : {}'.format(v)),
    ('maxLength', lambda v: 'Taille maximale : {}'.format(v)),
    ('minimum', lambda v: 'Valeur minimale : {}'.format(v)),
    ('maximum', lambda v: 'Valeur maximale : {}'.format(v)),
    ('pattern', lambda v: 'Motif : `{}`'.format(v)),
    ('enum', lambda v: 'Valeurs autorisées : {}'.format(", ".join(v))),
])


def format_format(format_val):
    """ Return markdown format information """
    return "- `{}` {}\n".format(format_val, FORMAT_MAP.get(format_val, ''))


def format_type_specific_info(col_content):
    """ Formats and return info relative to type """
    buff = io.StringIO()
    for prop in TYPE_SPECIFIC_MAP:
        if prop in col_content:
            buff.write('- {} : {}\n'.format(TYPE_SPECIFIC_MAP[prop], col_content[prop]))

    if 'bareNumber' in col_content and col_content['bareNumber'] == 'false':
        buff.write('- Le nombre peut contenir des caractères supplémentaires (« € », « % » ...)\n')
    ret = buff.getvalue()
    buff.close()
    return ret


def format_constraints(col_content):
    """ Converts type and constraints information into markdown """
    buff = io.StringIO()

    # Type
    type_ = col_content.get('type')
    format_ = col_content.get('format')

    if type_:
        type_val = TYPE_MAP.get(type_, '??{}??'.format(type_))
        buff.write('- Type : {}{}\n'.format(
            type_val,
            "" if format_ in ["default", None] else " (format `{}`)".format(format_)

        ))
        # Type specific properties
        buff.write(format_type_specific_info(col_content))

    # RDFType
    rdf_type = col_content.get('rdfType')
    if rdf_type:
        buff.write('- Type RDF : {}\n'.format(rdf_type))

    example = col_content.get('example')
    if example:
        buff.write('- Exemple : {}\n'.format(example))

    constraints = col_content.get('constraints')
    if constraints:
        required = None
        if constraints.get('required'):
            required = 'obligatoire'
        elif not constraints.get('required', True):
            required = 'optionnelle'
        constraint_str_list = list(filter(None, [
            required,
            'unique' if constraints.get('unique') else None,
        ]))
        if constraint_str_list:
            buff.write('- Valeur : {}\n'.format(",".join(constraint_str_list)))

        # minLength, maxLength, minimum, maximum, pattern, enum
        for prop in CONSTRAINTS_MAP:
            if prop in constraints:
                buff.write('- {}\n'.format(CONSTRAINTS_MAP[prop](constraints[prop])))

    ret = buff.getvalue()
    buff.close()
    return ret


def format_property(name, value):
    if name == "created":
        return datetime.fromisoformat(value).strftime("%x")
    return value


def convert_source(source, out_fd, schemas_config=None):
    log.info('Loading schema from %r', source)
    schema = json.load(open(source))

    convert_json(schema, out_fd)


def convert_json(schema_json, out_fd):
    """ Converts table schema data to markdown """

    # Header
    out_fd.write('## {}'.format(schema_json['title']))
    out_fd.write('\n\n')

    if 'description' in schema_json:
        out_fd.write(schema_json['description'])
        out_fd.write('\n\n')

    version = schema_json.get('version')
    if version:
        out_fd.write("## Version {}".format(version, ))
        out_fd.write('\n\n')

    for property_name in ('author', 'contributor', 'created', 'homepage', 'example'):
        property_value = schema_json.get(property_name)
        if property_value:
            out_fd.write('- {} : {}\n'.format(SCHEMA_PROP_MAP[property_name],
                                              format_property(property_name, property_value)))

    # Missing values
    missing_values = schema_json.get('missingValues')
    if missing_values:
        out_fd.write('- Valeurs manquantes : {}\n'.format(", ".join(map(lambda v: '`"{}"`'.format(v), missing_values))))

    # Primary key
    primary_key = schema_json.get('primaryKey')
    if primary_key:
        out_fd.write('- Clé primaire : `{}`\n'.format(
            ", ".join(primary_key) if isinstance(primary_key, list) else primary_key))

    # Foreign keys contraint is more complex than a list of strings, more work required.

    out_fd.write("\n\n")

    fields = schema_json.get('fields')
    if fields:
        out_fd.write('### Modèle de données\n\n')
        for field in fields:
            convert_field(field, out_fd)


def convert_field(field_json, out_fd):
    """ Convert json content describing a column to markdown """

    field_name = field_json.get('name')
    out_fd.write('#### {}\n\n'.format(
        "`{}`".format(field_name) if field_name else "Erreur : nom manquant"
    ))

    title = field_json.get('title')
    if title:
        out_fd.write("- Titre : {}\n".format(title))

    description = field_json.get('description')
    if description:
        out_fd.write("- Description : {}\n".format(description))

    out_fd.write(format_constraints(field_json))
    out_fd.write('\n')


def main():
    """Converts a table schema file into Markdown."""

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('table_schema', help='path or URL of table schema file')
    parser.add_argument('-o', '--output', help='Output file name', default='stdout')
    parser.add_argument('--log', default='WARNING', help='level of logging messages')
    args = parser.parse_args()

    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {}'.format(args.log))
    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(asctime)s:%(message)s",
        level=numeric_level,
        stream=sys.stdout, # Use stderr if script outputs data to stdout.
    )

    out_fd = sys.stdout if args.output == 'stdout' else open(args.output, mode='wt', encoding='UTF-8')

    convert_source(args.table_schema, out_fd)

if __name__ == '__main__':
    main()
