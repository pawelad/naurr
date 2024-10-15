"""naurr utils."""

from collections import defaultdict


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
    # TODO: Are the values unique?
    # TODO: Edge case: `"delivery_promotion": ["delivery_promotion_id"]`?
    prefixes_with_values = defaultdict(list)

    # For each value, find the potential prefixes
    for value in values:
        chunks = value.split(delimiter)

        for i in range(len(chunks)):
            prefix = delimiter.join(chunks[: i + 1])
            prefixes_with_values[prefix].append(value)

    # Filter to only prefixes with more than 1 occurrence and sort by the longest prefix
    filtered_prefixes_with_values = [
        key for key, value in prefixes_with_values.items() if len(value) > 1
    ]
    sorted_prefixes_with_values = sorted(
        filtered_prefixes_with_values,
        key=len,
        reverse=True,
    )

    processed_values = set()  # To keep track of values and avoid duplicates
    grouped_names = defaultdict(list)
    for prefix in sorted_prefixes_with_values:
        for value in prefixes_with_values[prefix]:
            if value not in processed_values:
                grouped_names[prefix].append(value)
                processed_values.add(value)

    return dict(grouped_names)
