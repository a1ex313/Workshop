from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from workshop import Create_tables
from .settings import settings
from .Create_tables import DatabaseCreate

print("database")
print("\n\n")
db = DatabaseCreate(settings.database_url)
db.check_db()
db.create_db()
print("\n\n")


engine = create_engine(settings.database_url)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)

def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()
