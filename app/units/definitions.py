from enum import Enum


class UnitCategory(str, Enum):
    MASS = "mass"
    VOLUME = "volume"
    TEMPERATURE = "temperature"
    COUNT = "count"


class Unit(str, Enum):
    # Mass
    MILLIGRAM = "mg"
    GRAM = "g"
    KILOGRAM = "kg"
    OUNCE = "oz"
    POUND = "lb"

    # Volume
    MILLILITER = "ml"
    LITER = "l"
    TEASPOON = "tsp"
    TABLESPOON = "tbsp"
    CUP = "cup"
    FLUID_OUNCE = "fl_oz"

    # Temperature
    CELSIUS = "c"
    FAHRENHEIT = "f"

    # Count
    PIECE = "piece"

    @property
    def category(self) -> UnitCategory:
        if self in {
            Unit.MILLIGRAM,
            Unit.GRAM,
            Unit.KILOGRAM,
            Unit.OUNCE,
            Unit.POUND,
        }:
            return UnitCategory.MASS

        if self in {
            Unit.MILLILITER,
            Unit.LITER,
            Unit.TEASPOON,
            Unit.TABLESPOON,
            Unit.CUP,
            Unit.FLUID_OUNCE,
        }:
            return UnitCategory.VOLUME

        if self in {
            Unit.CELSIUS,
            Unit.FAHRENHEIT,
        }:
            return UnitCategory.TEMPERATURE

        if self == Unit.PIECE:
            return UnitCategory.COUNT

        raise ValueError(f"Unknown unit: {self}")