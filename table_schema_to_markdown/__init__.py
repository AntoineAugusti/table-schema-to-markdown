# -*- coding: utf-8 -*-
import io
import json
import logging

from collections import OrderedDict
from datetime import datetime

NAME = "name"
TITLE = "title"
DESCRIPTION = "description"
PRIMARY_KEY = "primaryKey"
MISSING_VALUES = "missingValues"

AUTHOR = "author"
CONTRIBUTOR = "contributor"
VERSION = "version"
CREATED = "created"
HOMEPAGE = "homepage"
EXAMPLE = "example"

log = logging.getLogger(__name__)

SCHEMA_PROP_MAP = OrderedDict(
    [
        (AUTHOR, "Auteur"),
        (CONTRIBUTOR, "Contributeurs"),
        (CREATED, "Schéma créé le"),
        (HOMEPAGE, "Site web"),
        (EXAMPLE, "Données d'exemple"),
        (VERSION, "Version"),
    ]
)

TYPE_MAP = {
    "array": "liste",
    "boolean": "booléen",
    "date": "date",
    "datetime": "date et heure",
    "duration": "durée",
    "geojson": "GéoJSON",
    "geopoint": "point géographique",
    "integer": "nombre entier",
    "number": "nombre réel",
    "object": "objet",
    "string": "chaîne de caractères",
    "time": "heure",
    "year": "année",
    "year-month": "année et mois",
}

FORMAT_MAP = {
    "email": "adresse de courriel",
    "uri": "adresse URL",
    "binary": "données binaires encodées en base64",
    "uuid": "identifiant UUID",
}

TYPE_SPECIFIC_MAP = OrderedDict(
    [
        ("decimalChar", "Séparateur décimal («.» par défaut)"),
        ("groupChar", "Séparateur de groupes de chiffres («,» par défaut)"),
        # 'bareNumber' : 'Nombre nu', => Needs a specific treatment
        ("trueValues", "Valeurs considérées comme vraies"),
        ("falseValues", "Valeurs considérées comme fausses"),
    ]
)

CONSTRAINTS_MAP = OrderedDict(
    [
        ("minLength", lambda v: "Taille minimale : {}".format(v)),
        ("maxLength", lambda v: "Taille maximale : {}".format(v)),
        ("minimum", lambda v: "Valeur minimale : {}".format(v)),
        ("maximum", lambda v: "Valeur maximale : {}".format(v)),
        ("pattern", lambda v: "Motif : `{}`".format(v)),
        ("enum", lambda v: "Valeurs autorisées : {}".format(", ".join(v))),
    ]
)


def format_format(format_val):
    """ Return markdown format information """
    return "- `{}` {}\n".format(format_val, FORMAT_MAP.get(format_val, ""))


def format_type_specific_info(col_content):
    """ Formats and return info relative to type """
    buff = io.StringIO()
    for prop in TYPE_SPECIFIC_MAP:
        if prop in col_content:
            buff.write("{} : {}".format(TYPE_SPECIFIC_MAP[prop], col_content[prop]))

    if "bareNumber" in col_content and col_content["bareNumber"] == "false":
        buff.write(
            "Le nombre peut contenir des caractères supplémentaires (« € », « % » ...)"
        )
    ret = buff.getvalue()
    buff.close()
    return ret


def format_type(col_content):
    buff = io.StringIO()
    # Type
    type_ = col_content.get("type")
    format_ = col_content.get("format")

    if type_:
        type_val = TYPE_MAP.get(type_, "??{}??".format(type_))
        buff.write(
            "{}{}|".format(
                type_val,
                ""
                if format_ in ["default", None]
                else " (format `{}`)".format(format_),
            )
        )
        # Type specific properties
        buff.write(format_type_specific_info(col_content))

    # RDFType
    rdf_type = col_content.get("rdfType")
    if rdf_type:
        buff.write("{}|".format(rdf_type))

    ret = buff.getvalue()
    buff.close()
    return ret


def format_example(col_content):
    example = col_content.get(EXAMPLE)
    if example:
        return "{}|".format(example)

    return "|"


def format_constraints(col_content):
    """ Converts type and constraints information into Markdown """
    buff = io.StringIO()

    constraints = col_content.get("constraints")
    if constraints:
        required = None
        if constraints.get("required"):
            required = "Valeur obligatoire"
        elif not constraints.get("required", True):
            required = "Valeur optionnelle"
        constraint_str_list = list(
            filter(
                None, [required, "Valeur unique" if constraints.get("unique") else None]
            )
        )

        # minLength, maxLength, minimum, maximum, pattern, enum
        for prop in [prop for prop in CONSTRAINTS_MAP if prop in constraints]:
            constraint_str_list.append(CONSTRAINTS_MAP[prop](constraints[prop]))

        buff.write(", ".join(constraint_str_list))

    ret = buff.getvalue()
    buff.close()
    return ret


def format_property(name, value):
    if name == CREATED:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%x")
    if name == MISSING_VALUES:
        if value == [""]:
            return ""
        return ", ".join(map(lambda v: '`"{}"`'.format(v), value))
    if name == PRIMARY_KEY:
        return ", ".join(value) if isinstance(value, list) else value
    return value


def format_name(field_json):
    buff = io.StringIO()

    field_name = field_json.get("name")
    buff.write(
        "|{}".format("{}".format(field_name) if field_name else "Erreur : nom manquant")
    )

    title = field_json.get("title")
    if title:
        buff.write(" ({})".format(title))

    buff.write("|")

    ret = buff.getvalue()
    buff.close()
    return ret


def convert_source(source, out_fd):
    log.info("Loading schema from %r", source)
    with open(source, encoding="utf-8") as f:
        schema = json.load(f)

    convert_json(schema, out_fd)


def write_property(schema_json, property_name, out_fd, prefix="", suffix="\n\n"):
    if property_name in schema_json:
        propery_value = format_property(property_name, schema_json[property_name])
        if propery_value != "":
            out_fd.write(prefix + propery_value + suffix)


def convert_json(schema_json, out_fd):
    """ Converts table schema data to markdown """

    # Header
    if NAME in schema_json:
        write_property(schema_json, NAME, out_fd, "## ")
        write_property(schema_json, TITLE, out_fd)
    else:
        write_property(schema_json, TITLE, out_fd, "## ")
    write_property(schema_json, DESCRIPTION, out_fd)

    for property_name in SCHEMA_PROP_MAP.keys():
        prefix = "- {} : ".format(SCHEMA_PROP_MAP[property_name])
        write_property(schema_json, property_name, out_fd, prefix, "\n")

    write_property(schema_json, MISSING_VALUES, out_fd, "- Valeurs manquantes : ", "\n")
    write_property(schema_json, PRIMARY_KEY, out_fd, "- Clé primaire : `", "`\n")

    # Foreign keys constraint is more complex than a list of strings, more work required.

    out_fd.write("\n")

    fields = schema_json.get("fields")
    if fields:
        out_fd.write("### Modèle de données\n\n")
        # GitHub Flavored Markdown table header
        headers = ["Nom", "Type", "Description", "Exemple", "Propriétés"]
        out_fd.write("|" + "|".join(headers) + "|\n")
        out_fd.write("|" + "|".join("-" * len(headers)) + "|\n")
        for field in fields:
            convert_field(field, out_fd)


def format_description(field_json):
    description = field_json.get("description")
    if description:
        return "{}|".format(description)
    return ""


def convert_field(field_json, out_fd):
    """ Convert JSON content describing a column to Markdown"""

    out_fd.write(format_name(field_json))
    out_fd.write(format_type(field_json))
    out_fd.write(format_description(field_json))
    out_fd.write(format_example(field_json))
    out_fd.write(format_constraints(field_json))

    out_fd.write("|\n")
