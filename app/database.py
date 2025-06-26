from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL


engine = create_engine(DATABASE_URL)

session = sessionmaker(engine)

base = declarative_base()