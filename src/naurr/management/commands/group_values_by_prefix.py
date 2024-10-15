"""Helper command to group passed values by their common prefixes."""

import csv
import json
import pathlib
from typing import Any

from django.core.management import BaseCommand, CommandParser

from naurr.utils import group_by_prefix


def read_values_from_file(path: pathlib.Path) -> list[str]:
    """Read single word rows from a file and output it as a list.

    The file should be formatted as one word per line, i.e.:
    ```
    foo_bar
    foo_bar_baz
    baz
    ```

    Arguments:
        path: Path to the file.

    Returns:
        List of values read form the file.
    """
    values = []
    with open(path) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 0:
                values.append(row[0])

    return values


class Command(BaseCommand):
    """Helper command to group passed values by their common prefixes.

    It can receive the values either from a file ir passed as positional arguments.
    Passing both will combine the values. If the output file is provided, it will
    save the grouped values there in JSON format, otherwise they'll be written
    to stdout. A custom delimiter can be set to be used when finding potential
    value prefixes.
    """

    help = "Group passed values by their common prefixes."

    def add_arguments(self, parser: CommandParser) -> None:
        """Add custom `argparse` arguments."""
        parser.add_argument(
            "-i",
            "--input_file",
            type=pathlib.Path,
            help="Path to the input file.",
        )
        parser.add_argument(
            "-o",
            "--output_file",
            type=pathlib.Path,
            help="Path to the output JSON file.",
        )
        parser.add_argument(
            "-d",
            "--delimiter",
            type=str,
            default="_",
            help="Delimiter to use when finding potential value prefixes.",
        )
        parser.add_argument(
            "values",
            nargs="*",
            type=str,
            help="List of values to group.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Group passed values by their common prefixes.

        If both `input_file` and positional arguments are provided, combine them.
        If the `output_file` is passed, save the grouped values in JSON format,
        otherwise write it to stdout.
        """
        values = options["values"]

        input_file = options["input_file"]
        if input_file:
            input_file_values = read_values_from_file(input_file)
            values += input_file_values

        delimiter = options["delimiter"]
        grouped_values = group_by_prefix(values, delimiter=delimiter)

        grouped_values_json = json.dumps(grouped_values, indent=4)

        output_file = options["output_file"]
        if output_file:
            with open(output_file, "w") as f:
                f.write(grouped_values_json)
            self.stdout.write(
                self.style.SUCCESS(
                    f"> Successfully saved grouped values to '{output_file}'"
                )
            )
        else:
            self.stdout.write(grouped_values_json)
