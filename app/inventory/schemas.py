from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.units.definitions import Unit


def _blank_to_none(value):
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


class ProductCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=200)]
    brand: Annotated[str, Field(max_length=100)] | None = None
    barcode: Annotated[str, Field(max_length=100)] | None = None
    default_unit: Unit = Unit.PIECE
    notes: str | None = None

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value):
        # Strip first so "   " is rejected by min_length.
        return value.strip() if isinstance(value, str) else value

    @field_validator("brand", "barcode", "notes", mode="before")
    @classmethod
    def blank_to_none(cls, value):
        # Empty barcode must become NULL, otherwise two blanks collide on UNIQUE.
        return _blank_to_none(value)


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    brand: str | None
    barcode: str | None
    default_unit: str
    notes: str | None


class InventoryCreate(BaseModel):
    product_id: int
    # Matches Numeric(12, 3) in the model.
    quantity: Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=3)]
    unit: Unit
    expiration_date: date | None = None
    purchased_at: datetime | None = None
    opened_at: datetime | None = None
    notes: str | None = None

    @field_validator("notes", mode="before")
    @classmethod
    def blank_to_none(cls, value):
        return _blank_to_none(value)


class InventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product: ProductRead
    quantity: Decimal
    unit: str
    expiration_date: date | None
    purchased_at: datetime
    opened_at: datetime | None
    notes: str | None
