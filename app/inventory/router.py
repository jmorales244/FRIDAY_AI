from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.inventory.models import InventoryItem, Product
from app.inventory.schemas import (
    InventoryCreate,
    InventoryRead,
    ProductCreate,
    ProductRead,
)

router = APIRouter()


@router.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    stmt = select(Product).order_by(Product.name, Product.id)
    return db.scalars(stmt).all()


@router.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    if payload.barcode is not None:
        existing = db.scalar(
            select(Product.id).where(Product.barcode == payload.barcode)
        )
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A product with barcode '{payload.barcode}' already exists.",
            )

    product = Product(
        name=payload.name,
        brand=payload.brand,
        barcode=payload.barcode,
        default_unit=payload.default_unit.value,
        notes=payload.notes,
    )
    db.add(product)
    try:
        db.commit()
    except IntegrityError:
        # Race between the pre-check and the commit; the UNIQUE index is the
        # real guard.
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A product with barcode '{payload.barcode}' already exists.",
        )
    db.refresh(product)
    return product


@router.get("/inventory", response_model=list[InventoryRead])
def list_inventory(db: Session = Depends(get_db)):
    # Soonest-expiring first, items without an expiration date last, then id.
    stmt = (
        select(InventoryItem)
        .options(joinedload(InventoryItem.product))
        .order_by(
            InventoryItem.expiration_date.is_(None),
            InventoryItem.expiration_date,
            InventoryItem.id,
        )
    )
    return db.scalars(stmt).unique().all()


@router.post(
    "/inventory",
    response_model=InventoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_inventory_item(payload: InventoryCreate, db: Session = Depends(get_db)):
    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {payload.product_id} not found.",
        )

    item = InventoryItem(
        product_id=product.id,
        quantity=payload.quantity,
        unit=payload.unit.value,
        expiration_date=payload.expiration_date,
        purchased_at=payload.purchased_at or datetime.utcnow(),
        opened_at=payload.opened_at,
        notes=payload.notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
