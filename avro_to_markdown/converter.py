class AvroToMarkdownFailure(Exception):
    pass


# Non-technical descriptions of field types

FIELD_TYPE_DESCRIPTIONS = {
    "int": "number",
    "long": "number",
    "double": "number",
    "null": "missing",
    "boolean": "yes/no",
    "string": "text",
}


def is_record(type_field):
    """
    Is the avro field a record or a non record?
    Non-records return true. Fields that are scalar, null *or* a record
    also return True.
    """
    if isinstance(type_field, list):
        for avro_type in type_field:
            if isinstance(avro_type, dict):
                if avro_type.get("type") == "record":
                    return True
        return False
    else:
        if isinstance(type_field, dict):
            return type_field.get("type") == "record"
        else:
            return False


def subfields(type_field):
    """
    Get a list of sub-fields from an avro record field.
    """
    if isinstance(type_field, dict):
        return type_field
    else:
        for avro_type in type_field:
            if isinstance(avro_type, dict):
                return avro_type


def described_field_type(singular_type_field):
    """
    Human readable equivalent of a singular avro type - e.g. long -> number.
    """
    if isinstance(singular_type_field, dict):
        if "logicalType" in singular_type_field:
            return singular_type_field["logicalType"]
        else:
            if singular_type_field.get("type") == "array":
                return described_field_type(singular_type_field["items"]) + " list"
            elif singular_type_field.get("type") in ("enum", "record"):
                return singular_type_field["name"]
            else:
                raise AvroToMarkdownFailure(
                    "Did not understand " + str(singular_type_field)
                )
    else:
        if singular_type_field in FIELD_TYPE_DESCRIPTIONS:
            return FIELD_TYPE_DESCRIPTIONS[singular_type_field]
        else:
            raise AvroToMarkdownFailure(
                "Did not understand " + str(singular_type_field)
            )


def described_field_types(type_field):
    """
    Human readable equivalent of an avro type or list of types - long, type, null, etc.
    Displays either a 'or' separated list or the single field type.
    """
    if isinstance(type_field, list):
        return " or ".join(
            described_field_type(singular_type) for singular_type in type_field
        )
    else:
        return described_field_type(type_field)


def schema_to_markdown(heading: str, schema_json: dict):
    """
    Output a human readable markdown version of a parsed JSON avro schema.
    """
    markdown = heading

    for field in schema_json["fields"]:
        if is_record(field["type"]):
            markdown += f"\n\n# **{field['name']}** - {field['doc']}\n\n"

            for subfield in subfields(field["type"])["fields"]:
                try:
                    markdown += f"* **{subfield['name']}** - {subfield['doc']} ({described_field_types(subfield['type'])})\n"
                except KeyError:
                    markdown += f"* **{subfield['name']}** ({described_field_types(subfield['type'])})\n"

        else:
            try:
                markdown += f"* {field['name']} - {field['doc']} ({described_field_types(field['type'])})\n"
            except KeyError:
                markdown += (
                    f"* {field['name']} ({described_field_types(field['type'])})\n"
                )

    return markdown
