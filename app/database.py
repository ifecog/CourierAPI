from databases import Database

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

from decouple import config


DATABASE_USERNAME = config("DATABASE_USERNAME")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_HOST = config("DATABASE_HOST")
DATABASE_PORT = config("DATABASE_PORT")
DATABASE_NAME = config("DATABASE_NAME")

def get_sqlalchemy_url():
    return f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    
DATABASE_URL = get_sqlalchemy_url()

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Base = declarative_base()