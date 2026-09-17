from dataclasses import dataclass
from decimal import Decimal

from app.units.definitions import Unit
from app.units.conversions import (
    convert_mass,
    convert_volume,
    convert_temperature,
)


@dataclass(frozen=True)
class Quantity:
    value: Decimal
    unit: Unit

    def __post_init__(self):
        if not isinstance(self.value, Decimal):
            object.__setattr__(self, "value", Decimal(str(self.value)))

    def __str__(self):
        return f"{self.value} {self.unit.value}"

    def convert_to(self, target_unit: Unit) -> "Quantity":
        if self.unit == target_unit:
            return self

        if self.unit.category != target_unit.category:
            raise ValueError(
                f"Cannot convert {self.unit.value} to {target_unit.value}"
            )

        if self.unit.category.value == "mass":
            new_value = convert_mass(
                self.value,
                self.unit,
                target_unit,
            )

        elif self.unit.category.value == "volume":
            new_value = convert_volume(
                self.value,
                self.unit,
                target_unit,
            )

        elif self.unit.category.value == "temperature":
            new_value = convert_temperature(
                self.value,
                self.unit,
                target_unit,
            )

        else:
            raise ValueError(
                f"Conversion not supported for category: "
                f"{self.unit.category.value}"
            )

        return Quantity(new_value, target_unit)