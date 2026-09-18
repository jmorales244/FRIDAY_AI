from decimal import Decimal

import pytest

from app.units.definitions import Unit
from app.units.quantity import Quantity


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