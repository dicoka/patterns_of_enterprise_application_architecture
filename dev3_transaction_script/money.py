from decimal import Decimal, ROUND_DOWN
from functools import cached_property

amount_number = Decimal | int | float

class Money:
    def __init__(self, amount: amount_number, currency: str):
        self._initial_amount = amount
        self._currency = currency

    @classmethod
    def dollars(cls, amount: amount_number) -> "Money":
        return cls(amount, "USD")

    @cached_property
    def amount(self) -> Decimal:
        return round(Decimal(self._initial_amount), 2)

    @property
    def currency(self) -> str:
        return self._currency

    def allocate(self, num_of_parts: int) -> list["Money"]:
        low = Decimal(self.amount / num_of_parts).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        high = low + Decimal("0.01")
        remainder = int(100 * (self.amount - low * num_of_parts))

        low = Money(low, self.currency)
        high = Money(high, self.currency)
        return [high] * remainder + [low] * (num_of_parts - remainder)

    def __eq__(self, other):
        try:
            self._validate_other(other)
        except ValueError:
            return False
        return self.amount == other.amount

    def __add__(self, other):
        other = self._prepare_other(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        other = self._prepare_other(other)
        return Money(self.amount - other.amount, self.currency)

    def _prepare_other(self, other):
        if isinstance(other, Decimal):
            return Money(other, self.currency)
        self._validate_other(other)
        return other

    def _validate_other(self, other):
        if not isinstance(other, Money):
            raise ValueError(f"Not allowed for {type(other)}")

        if self.currency != other.currency:
            raise ValueError("Currency mismatch")

    def __repr__(self):
        return f"Money({self.amount}, {self.currency})"
