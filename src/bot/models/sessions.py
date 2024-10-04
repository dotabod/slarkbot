from sqlalchemy.orm import sessionmaker
from . import create_database_engine

engine = None


def create_session():
    global engine  # Declare engine as global to modify the module-level variable

    # TODO: this is a hack, want engine singleton but its python ..
    if engine is None:
        engine = create_database_engine()

    session = sessionmaker()
    session.configure(bind=engine)
    return session()
