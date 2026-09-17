from decimal import Decimal

from app.units.definitions import Unit


# Conversion factors to canonical units.
#
# Canonical mass unit: gram
# Canonical volume unit: milliliter


MASS_TO_GRAMS = {
    Unit.MILLIGRAM: Decimal("0.001"),
    Unit.GRAM: Decimal("1"),
    Unit.KILOGRAM: Decimal("1000"),
    Unit.OUNCE: Decimal("28.349523125"),
    Unit.POUND: Decimal("453.59237"),
}


VOLUME_TO_ML = {
    Unit.MILLILITER: Decimal("1"),
    Unit.LITER: Decimal("1000"),
    Unit.TEASPOON: Decimal("4.92892159375"),
    Unit.TABLESPOON: Decimal("14.78676478125"),
    Unit.CUP: Decimal("236.588236996"),
    Unit.FLUID_OUNCE: Decimal("29.5735295625"),
}


def convert_mass(
    value: Decimal | float | int,
    from_unit: Unit,
    to_unit: Unit,
) -> Decimal:
    if from_unit not in MASS_TO_GRAMS:
        raise ValueError(f"{from_unit} is not a mass unit.")

    if to_unit not in MASS_TO_GRAMS:
        raise ValueError(f"{to_unit} is not a mass unit.")

    value = Decimal(str(value))

    grams = value * MASS_TO_GRAMS[from_unit]

    return grams / MASS_TO_GRAMS[to_unit]


def convert_volume(
    value: Decimal | float | int,
    from_unit: Unit,
    to_unit: Unit,
) -> Decimal:
    if from_unit not in VOLUME_TO_ML:
        raise ValueError(f"{from_unit} is not a volume unit.")

    if to_unit not in VOLUME_TO_ML:
        raise ValueError(f"{to_unit} is not a volume unit.")

    value = Decimal(str(value))

    milliliters = value * VOLUME_TO_ML[from_unit]

    return milliliters / VOLUME_TO_ML[to_unit]


def convert_temperature(
    value: Decimal | float | int,
    from_unit: Unit,
    to_unit: Unit,
) -> Decimal:
    value = Decimal(str(value))

    if from_unit == Unit.CELSIUS and to_unit == Unit.FAHRENHEIT:
        return (value * Decimal("9") / Decimal("5")) + Decimal("32")

    if from_unit == Unit.FAHRENHEIT and to_unit == Unit.CELSIUS:
        return (value - Decimal("32")) * Decimal("5") / Decimal("9")

    if from_unit == to_unit:
        return value

    raise ValueError(
        f"Cannot convert temperature from {from_unit} to {to_unit}."
    )