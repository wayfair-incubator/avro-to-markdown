from avro_to_markdown import schema_to_markdown
from avro_to_markdown.converter import described_field_types, is_record, subfields


def test_schema_to_markdown():
    schema = {
        "type": "record",
        "name": "User",
        "namespace": "example.avro",
        "fields": [
            {"name": "favorite_number", "type": "int", "doc": "Favorite number"}
        ],
    }

    assert (
        schema_to_markdown("# Heading\n", schema)
        == "# Heading\n* favorite_number - Favorite number (number)\n"
    )


def test_descriptive_scalar_field_types():
    assert described_field_types(["null", "long"]) == "missing or number"
    assert described_field_types(["null", "boolean"]) == "missing or yes/no"
    assert described_field_types(["null", "string"]) == "missing or text"


def test_logical_types():
    assert (
        described_field_types(
            ["null", {"type": "long", "logicalType": "timestamp-millis"}]
        )
        == "missing or timestamp-millis"
    )


def test_describe_array_of_types():
    assert (
        described_field_types(
            ["null", {"type": "array", "items": {"type": "int", "logicalType": "date"}}]
        )
        == "missing or date list"
    )


def test_describe_enum():
    assert (
        described_field_types(
            [
                "null",
                {
                    "type": "array",
                    "items": {
                        "type": "enum",
                        "name": "favorite_days_of_the_week",
                        "symbols": [
                            "Monday",
                            "Tuesday",
                            "Wednesday",
                            "Thursday",
                            "Friday",
                            "Saturday",
                            "Sunday",
                        ],
                    },
                },
            ]
        )
        == "missing or favorite_days_of_the_week list"
    )


def test_describe_record():
    assert (
        described_field_types(
            ["null", {"type": "record", "name": "favorite color", "fields": []}]
        )
        == "missing or favorite color"
    )


def test_non_record():
    """
    Record types contain a dict with type field record.
    """
    assert not is_record(["null", "boolean"])


def test_record_is_record():
    """
    Record types contain a dict with type field record.
    """
    assert is_record(
        [
            "null",  # Is this null because we don't care about the schema itself?
            {
                "type": "record",
                "name": "User",
                "fields": [
                    {
                        "name": "favorite_color",
                        "doc": "The user's favorite color.",
                        "type": ["null", "str"],
                    }
                ],
            },
        ]
    )


def test_subfields():
    schema_chunk = [
        "null",
        {
            "type": "record",
            "name": "User",
            "fields": [
                {
                    "name": "favorite_number",
                    "doc": "The user's favorite number.",
                    "type": ["null", "int"],
                }
            ],
        },
    ]
    assert subfields(schema_chunk) == {
        "type": "record",
        "name": "User",
        "fields": [
            {
                "name": "favorite_number",
                "doc": "The user's favorite number.",
                "type": ["null", "int"],
            }
        ],
    }
