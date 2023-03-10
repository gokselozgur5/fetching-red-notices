import logging
from dotenv import load_dotenv
from sqlalchemy import JSON, create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


logging.basicConfig(level=logging.DEBUG)


try:
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_dotenv(dotenv_path)
except Exception as e:
    # exception object might be more specific
    logging.error(f'environment file could not be loaded! \n{e}')

# Get database connection parameters from environment variables
db_host = os.getenv('POSTGRES_HOST')
db_port = int(os.getenv('POSTGRES_PORT'))
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')

# Create a database engine
db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_uri)

# Create a session factory
Session = sessionmaker(bind=engine)

# Define a database model
Base = declarative_base()


class MyTable(Base):
    __tablename__ = db_name
    id = Column(Integer, primary_key=True)
    data = Column(JSON)


class DatabaseManager:

    def __init__(self):
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def insert_list_to_table(self, my_list) -> None:
        with self.Session() as session:
            record = MyTable(data=my_list)
            session.add(record)
            session.commit()
            session.refresh(record)

    def get_items_from_table(self) -> list:
        with self.Session() as session:
            items = session.query(MyTable).all()
            item_list = [item.item for item in items]
            return item_list

