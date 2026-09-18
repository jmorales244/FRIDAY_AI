import re
from decimal import Decimal

from app.units.definitions import Unit
from app.units.quantity import Quantity


UNIT_ALIASES = {
    # Mass
    "mg": Unit.MILLIGRAM,
    "milligram": Unit.MILLIGRAM,
    "milligrams": Unit.MILLIGRAM,

    "g": Unit.GRAM,
    "gram": Unit.GRAM,
    "grams": Unit.GRAM,

    "kg": Unit.KILOGRAM,
    "kilo": Unit.KILOGRAM,
    "kilos": Unit.KILOGRAM,
    "kilogram": Unit.KILOGRAM,
    "kilograms": Unit.KILOGRAM,

    "oz": Unit.OUNCE,
    "ounce": Unit.OUNCE,
    "ounces": Unit.OUNCE,

    "lb": Unit.POUND,
    "lbs": Unit.POUND,
    "pound": Unit.POUND,
    "pounds": Unit.POUND,

    # Volume
    "ml": Unit.MILLILITER,
    "milliliter": Unit.MILLILITER,
    "milliliters": Unit.MILLILITER,

    "l": Unit.LITER,
    "liter": Unit.LITER,
    "liters": Unit.LITER,

    "tsp": Unit.TEASPOON,
    "teaspoon": Unit.TEASPOON,
    "teaspoons": Unit.TEASPOON,

    "tbsp": Unit.TABLESPOON,
    "tablespoon": Unit.TABLESPOON,
    "tablespoons": Unit.TABLESPOON,

    "cup": Unit.CUP,
    "cups": Unit.CUP,

    "fl oz": Unit.FLUID_OUNCE,
    "fl_oz": Unit.FLUID_OUNCE,
    "fluid ounce": Unit.FLUID_OUNCE,
    "fluid ounces": Unit.FLUID_OUNCE,

    # Temperature
    "c": Unit.CELSIUS,
    "celsius": Unit.CELSIUS,

    "f": Unit.FAHRENHEIT,
    "fahrenheit": Unit.FAHRENHEIT,

    # Count
    "piece": Unit.PIECE,
    "pieces": Unit.PIECE,
}


def parse_unit(text: str) -> Unit:
    """Convert a human-readable unit alias into a Unit enum."""

    normalized = text.strip().lower()

    try:
        return UNIT_ALIASES[normalized]
    except KeyError:
        raise ValueError(f"Unknown unit: {text}")


def parse_quantity(text: str) -> Quantity:
    """Convert a human-readable quantity into a Quantity object."""

    normalized = text.strip()

    match = re.fullmatch(
        r"([0-9]+(?:\.[0-9]+)?)\s*(.+)",
        normalized,
    )

    if not match:
        raise ValueError(f"Invalid quantity: {text}")

    value_text, unit_text = match.groups()

    try:
        value = Decimal(value_text)
    except Exception:
        raise ValueError(f"Invalid quantity value: {value_text}")

    unit = parse_unit(unit_text)

    return Quantity(value, unit)
