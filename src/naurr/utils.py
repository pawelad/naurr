"""naurr app utils."""

import itertools
from collections import defaultdict

from django.db import models


class BaseModel(models.Model):
    """Base Django model with shared fields."""

    created_at = models.DateTimeField(
        verbose_name="created at",
        auto_now_add=True,
    )

    modified_at = models.DateTimeField(
        verbose_name="modified at",
        auto_now=True,
    )

    class Meta:
        abstract = True


def group_by_prefix(values: list[str], *, delimiter: str = "_") -> dict[str, list[str]]:
    """Group passed values by their common prefixes.

    The grouping is as descriptive as possible (prefix of 'foo_bar_abc' and
    'foo_bar_xyz' is foo_bar). The groups aren't nested.

    Arguments:
        values: Values to group.
        delimiter: Delimiter to use when finding potential value prefixes.

    Returns:
        Passed values grouped by their common prefixes.
    """
    prefixes_with_values = defaultdict(list)

    # For each value, find the potential prefixes
    for value in values:
        chunks = value.split(delimiter)

        for i in range(len(chunks)):
            prefix = delimiter.join(chunks[: i + 1])
            prefixes_with_values[prefix].append(value)

    # We now want to separate the potential prefixes into two categories:
    # - prefixes with at least 2 matches, which we want to order by longest prefix
    # - prefixes with 1 match, witch we want to order by shortest prefix
    prefixes_multiple_matches = []
    prefixes_single_match = []
    for prefix, values in prefixes_with_values.items():
        if len(values) > 1:
            prefixes_multiple_matches.append(prefix)
        else:
            prefixes_single_match.append(prefix)

    prefixes_multiple_matches.sort(key=len, reverse=True)
    prefixes_single_match.sort(key=len, reverse=False)

    # Iterate over prefixes and group the values
    processed_values = set()  # To keep track of values and avoid duplicates
    grouped_names = defaultdict(list)
    for prefix in itertools.chain(prefixes_multiple_matches, prefixes_single_match):
        for value in prefixes_with_values[prefix]:
            if value not in processed_values:
                grouped_names[prefix].append(value)
                processed_values.add(value)

    # Unfortunately, we still end up with an edge case where `delivery_promotion_id`
    # is grouped as a single value under `delivery_promotion` and not `delivery`
    # if there were other values with potential `delivery_promotion` prefix.
    # TODO: Can this be done better?
    groups_with_single_values = {
        group_name: values
        for group_name, values in grouped_names.items()
        if len(values) == 1
    }

    for group_name, values in groups_with_single_values.items():
        group_name_chunks = group_name.split(delimiter)

        for i in range(len(group_name_chunks) - 1, 0, -1):
            prefix = delimiter.join(group_name_chunks[:i])

            if prefix in grouped_names or i == 1:
                grouped_names[prefix].append(values[0])
                del grouped_names[group_name]
                continue

    return dict(grouped_names)
