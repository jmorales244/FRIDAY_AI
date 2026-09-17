from app.database import engine
from app.inventory.models import Base


def init_database():
    Base.metadata.create_all(bind=engine)
    print("Kitchen AI database initialized.")


if __name__ == "__main__":
    init_database()