from app.db.database import get_connection
from app.db.schema import SCHEMA


def init_db():
    with get_connection() as connection:
        connection.executescript(SCHEMA)