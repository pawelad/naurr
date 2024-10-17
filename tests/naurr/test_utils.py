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
            "source",
        ],
        {
            "adhoc_charge_amt": ["adhoc_charge_amt", "adhoc_charge_amt_usd"],
            "admin_refund_amt": ["admin_refund_amt", "admin_refund_amt_usd"],
            "source": ["source"],
        },
    ),
    # If there's only one value in a group, we want it to be the least descriptive
    (
        [
            "delivery_promotion_discount_amt",
            "delivery_promotion_discount_amt_usd",
            "delivery_promotion_id",
        ],
        {
            "delivery_promotion_discount_amt": [
                "delivery_promotion_discount_amt",
                "delivery_promotion_discount_amt_usd",
            ],
            "delivery": ["delivery_promotion_id"],
        },
    ),
    # In this case, we want `delivery_promotion_id` to be grouped under `delivery`
    # and not `delivery_promotion`
    (
        [
            "delivery_promotion_discount_amt",
            "delivery_promotion_discount_amt_usd",
            "delivery_promotion_id",
            "delivery_fee_modifier",
            "delivery_type",
        ],
        {
            "delivery_promotion_discount_amt": [
                "delivery_promotion_discount_amt",
                "delivery_promotion_discount_amt_usd",
            ],
            "delivery": [
                "delivery_fee_modifier",
                "delivery_type",
                "delivery_promotion_id",
            ],
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
