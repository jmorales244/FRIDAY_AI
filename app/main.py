from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.inventory.router import router as inventory_router

app = FastAPI(title="FRIDAY_AI", version="0.2.0")

# Note: no table creation here. Run `python -m app.init_db` deliberately.
app.include_router(inventory_router)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """App availability is implied by a response; database is checked separately."""
    try:
        db.execute(text("SELECT 1"))
        database = "ok"
    except SQLAlchemyError:
        database = "unavailable"
    return {"status": "ok", "database": database}
