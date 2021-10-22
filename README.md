# Avro to Markdown

[![CI pipeline status](https://github.com/wayfair-incubator/avro-to-markdown/workflows/CI/badge.svg?branch=main)](https://github.com/wayfair-incubator/avro-to-markdown/actions/workflows/main.yml)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/wayfair-incubator/avro-to-markdown/blob/main/CODE_OF_CONDUCT.md)

## About The Project

Avro to markdown is a very simple project that generates readable markdown from an avro schema. This is useful
to be able to generate readable, always up-to-date documentation on the schemas you use to exchange messages within
your organization.

## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

```sh
pip install avro-to-markdown
```

## Usage

With avro_schema.avsc:

```json
{
    "type": "record",
    "name": "User",
    "namespace": "example.avro",
    "fields": [
        {"name": "favorite_number", "type": "int", "doc": "Favorite number"}
    ]
}
```

```python
>>> from pathlib import Path
>>> from avro_to_markdown import schema_to_markdown
>>> schema = json.loads(Path("avro_schema.avsc").read_text())
>>> print(schema_to_markdown("# My schema\n\nThis message has my favorite number.\n", schema))
```

```text
# My schema

This message has my favorite number.

* favorite_number - Favorite number (number)
```

## Roadmap

See the [open issues](https://github.com/wayfair-incubator/avro-to-markdown/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. For detailed contributing guidelines, please see [CONTRIBUTING.md](https://github.com/wayfair-incubator/avro-to-markdown/blob/main/CONTRIBUTING.md)

## License

Distributed under the `MIT` License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/wayfair-incubator/avro-to-markdown/](https://github.com/wayfair-incubator/avro-to-markdown/)
