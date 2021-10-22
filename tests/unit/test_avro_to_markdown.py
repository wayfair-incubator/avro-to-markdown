from avro_to_markdown import schema_to_markdown
from avro_to_markdown.converter import (
    _described_field_types,
    _is_record,
    _subfields,
)


def test_schema_to_markdown():
    """Check that markdown for 'favorite_number' entry is correctly generated."""
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
    """Check that correct description is generated for scalar field types."""
    assert _described_field_types(["null", "long"]) == "missing or number"
    assert _described_field_types(["null", "boolean"]) == "missing or yes/no"
    assert _described_field_types(["null", "string"]) == "missing or text"


def test_logical_types():
    """Check that correct description is generated for logical field types."""
    assert (
        _described_field_types(
            ["null", {"type": "long", "logicalType": "timestamp-millis"}]
        )
        == "missing or timestamp-millis"
    )


def test_describe_array_of_types():
    """Check that correct description is generated for an array of types."""
    assert (
        _described_field_types(
            [
                "null",
                {
                    "type": "array",
                    "items": {"type": "int", "logicalType": "date"},
                },
            ]
        )
        == "missing or date list"
    )


def test_describe_enum():
    """
    Check that correct description is generated for an array of enum field types.
    """
    assert (
        _described_field_types(
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
    """Check that correct description is generated for an individual record."""
    assert (
        _described_field_types(
            ["null", {"type": "record", "name": "favorite color", "fields": []}]
        )
        == "missing or favorite color"
    )


def test_non_record():
    """
    Record types contain a dict with type field record.
    """
    assert not _is_record(["null", "boolean"])


def test_record_is_record():
    """
    Record types contain a dict with type field record.
    """
    assert _is_record(
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
    """Check that subfields are correctly parsed from a schema."""
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
    assert _subfields(schema_chunk) == {
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
