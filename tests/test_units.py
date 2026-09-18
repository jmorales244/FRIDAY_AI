from decimal import Decimal

import pytest

from app.units.definitions import Unit
from app.units.quantity import Quantity
from app.units.parser import parse_unit


def test_quantity_creation():
    quantity = Quantity(350, Unit.GRAM)

    assert quantity.value == Decimal("350")
    assert quantity.unit == Unit.GRAM
    assert str(quantity) == "350 g"


def test_mass_conversion():
    quantity = Quantity(500, Unit.GRAM)

    kilograms = quantity.convert_to(Unit.KILOGRAM)
    ounces = quantity.convert_to(Unit.OUNCE)

    assert kilograms.value == Decimal("0.5")
    assert kilograms.unit == Unit.KILOGRAM

    assert ounces.value == Decimal("17.63698097479020645783790411")
    assert ounces.unit == Unit.OUNCE


def test_volume_conversion():
    quantity = Quantity(2, Unit.LITER)

    milliliters = quantity.convert_to(Unit.MILLILITER)

    assert milliliters.value == Decimal("2000")
    assert milliliters.unit == Unit.MILLILITER


def test_temperature_conversion():
    temperature = Quantity(400, Unit.FAHRENHEIT)

    celsius = temperature.convert_to(Unit.CELSIUS)

    assert celsius.value == Decimal("204.4444444444444444444444444")
    assert celsius.unit == Unit.CELSIUS


def test_quantity_addition_same_unit():
    chicken1 = Quantity(500, Unit.GRAM)
    chicken2 = Quantity(750, Unit.GRAM)

    total = chicken1 + chicken2

    assert total.value == Decimal("1250")
    assert total.unit == Unit.GRAM


def test_quantity_addition_different_units_same_category():
    chicken1 = Quantity(500, Unit.GRAM)
    chicken2 = Quantity(0.5, Unit.KILOGRAM)

    total = chicken1 + chicken2

    assert total.value == Decimal("1000.0")
    assert total.unit == Unit.GRAM


def test_quantity_subtraction_different_units_same_category():
    total = Quantity(1, Unit.KILOGRAM)
    used = Quantity(250, Unit.GRAM)

    remaining = total - used

    assert remaining.value == Decimal("0.75")
    assert remaining.unit == Unit.KILOGRAM


def test_incompatible_addition_raises_error():
    grams = Quantity(500, Unit.GRAM)
    milliliters = Quantity(500, Unit.MILLILITER)

    with pytest.raises(
        ValueError,
        match="Cannot add g and ml",
    ):
        grams + milliliters


def test_incompatible_subtraction_raises_error():
    grams = Quantity(500, Unit.GRAM)
    milliliters = Quantity(500, Unit.MILLILITER)

    with pytest.raises(
        ValueError,
        match="Cannot subtract ml from g",
    ):
        grams - milliliters


def test_quantity_uses_decimal():
    quantity = Quantity(0.1, Unit.KILOGRAM)

    assert isinstance(quantity.value, Decimal)
    assert quantity.value == Decimal("0.1")


def test_same_unit_conversion_returns_same_quantity():
    quantity = Quantity(500, Unit.GRAM)

    converted = quantity.convert_to(Unit.GRAM)

    assert converted is quantity


def test_parse_mass_unit_aliases():
    assert parse_unit("g") == Unit.GRAM
    assert parse_unit("gram") == Unit.GRAM
    assert parse_unit("grams") == Unit.GRAM

    assert parse_unit("kg") == Unit.KILOGRAM
    assert parse_unit("kilo") == Unit.KILOGRAM
    assert parse_unit("kilos") == Unit.KILOGRAM
    assert parse_unit("kilogram") == Unit.KILOGRAM
    assert parse_unit("kilograms") == Unit.KILOGRAM


def test_parse_volume_unit_aliases():
    assert parse_unit("ml") == Unit.MILLILITER
    assert parse_unit("milliliter") == Unit.MILLILITER
    assert parse_unit("milliliters") == Unit.MILLILITER

    assert parse_unit("l") == Unit.LITER
    assert parse_unit("liter") == Unit.LITER
    assert parse_unit("liters") == Unit.LITER


def test_parse_cooking_unit_aliases():
    assert parse_unit("tsp") == Unit.TEASPOON
    assert parse_unit("teaspoon") == Unit.TEASPOON
    assert parse_unit("teaspoons") == Unit.TEASPOON

    assert parse_unit("tbsp") == Unit.TABLESPOON
    assert parse_unit("tablespoon") == Unit.TABLESPOON
    assert parse_unit("tablespoons") == Unit.TABLESPOON


def test_parse_count_unit_aliases():
    assert parse_unit("piece") == Unit.PIECE
    assert parse_unit("pieces") == Unit.PIECE


def test_parse_unit_aliases_are_case_insensitive():
    assert parse_unit("G") == Unit.GRAM
    assert parse_unit("GRAMS") == Unit.GRAM
    assert parse_unit("Kg") == Unit.KILOGRAM
    assert parse_unit("ML") == Unit.MILLILITER
    assert parse_unit("Liters") == Unit.LITER
    assert parse_unit("TSP") == Unit.TEASPOON
    assert parse_unit("TBSP") == Unit.TABLESPOON
    assert parse_unit("Pieces") == Unit.PIECE

