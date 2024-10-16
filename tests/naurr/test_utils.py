"""Test `naurr.utils` module."""

import pytest

from naurr.utils import group_by_prefix

test_data = [
    # Group names should be as descriptive as possible
    (
        [
            "adhoc_charge_amt",
            "adhoc_charge_amt_usd",
            "admin_refund_amt",
            "admin_refund_amt_usd",
        ],
        {
            "adhoc_charge_amt": ["adhoc_charge_amt", "adhoc_charge_amt_usd"],
            "admin_refund_amt": ["admin_refund_amt", "admin_refund_amt_usd"],
        },
    ),
]


@pytest.mark.parametrize(("values", "grouped_values"), test_data)
def test_group_by_prefix(
    values: list[str],
    grouped_values: dict[str, list[str]],
) -> None:
    """Values are grouped into expected format."""
    assert group_by_prefix(values) == grouped_values
