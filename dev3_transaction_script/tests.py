from decimal import Decimal
from unittest import TestCase

from parameterized import parameterized

from dev3_transaction_script.money import Money


class TestMoney(TestCase):
    @parameterized.expand([
        (99.33,  [33.11, 33.11, 33.11]),
        (100.00, [33.34, 33.33, 33.33]),
        (100.01, [33.34, 33.34, 33.33]),
        (100.02, [33.34, 33.34, 33.34]),
        (100.03, [33.35, 33.34, 33.34]),
    ])
    def test_allocation(self, amount, expected_parts):
        money = Money(Decimal(amount), "USD")
        parts = money.allocate(len(expected_parts))
        self.assertEqual(
            list([Money(amount, "USD") for amount in expected_parts]),
            parts,
        )

