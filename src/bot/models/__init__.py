import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


def create_database_engine():
    db_url = os.getenv("POSTGRES_URL")

    connection_string = (
        f"{db_url}"
    )
    database_engine = create_engine(connection_string)
    return database_engine
