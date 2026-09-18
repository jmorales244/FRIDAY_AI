from dataclasses import dataclass
from decimal import Decimal

from app.units.definitions import Unit, UnitCategory
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
                f"Cannot convert {self.unit.value} to {target_unit.value}: "
                "units belong to different categories"
            )

        if self.unit.category == UnitCategory.MASS:
            new_value = convert_mass(
                self.value,
                self.unit,
                target_unit,
            )

        elif self.unit.category == UnitCategory.VOLUME:
            new_value = convert_volume(
                self.value,
                self.unit,
                target_unit,
            )

        elif self.unit.category == UnitCategory.TEMPERATURE:
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

    def __add__(self, other: "Quantity") -> "Quantity":
        if not isinstance(other, Quantity):
            return NotImplemented

        if self.unit.category != other.unit.category:
            raise ValueError(
                f"Cannot add {self.unit.value} and {other.unit.value}: "
                "units belong to different categories"
            )

        other_converted = other.convert_to(self.unit)

        return Quantity(
            self.value + other_converted.value,
            self.unit,
        )

    def __sub__(self, other: "Quantity") -> "Quantity":
        if not isinstance(other, Quantity):
            return NotImplemented

        if self.unit.category != other.unit.category:
            raise ValueError(
                f"Cannot subtract {other.unit.value} from {self.unit.value}: "
                "units belong to different categories"
            )

        other_converted = other.convert_to(self.unit)

        return Quantity(
            self.value - other_converted.value,
            self.unit,
        )