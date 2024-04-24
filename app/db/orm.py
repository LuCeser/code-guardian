from sqlmodel import SQLModel, create_engine, Session

# Create an SQLite URL for SQLAlchemy
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Function to get a database session
def get_session():
    with Session(engine) as session:
        yield session
