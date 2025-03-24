from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def get_session() -> sessionmaker:
    """
        Create and return a sessionmaker object for a local database session.

        Returns:
            sessionmaker: A sessionmaker object configured for the local database session.
    """
    #TODO: Move the hardcoded URL
    engine = create_engine('sqlite:///database.db')

    # Connect to the database and execute PRAGMA to enable foreign key constraints
    with engine.connect() as connection:
        # Enable foreign key constraints
        connection.execute(text('PRAGMA foreign_keys = ON;'))

    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session