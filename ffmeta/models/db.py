from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from ffmeta.settings import SQLALCHEMY_DATABASE_URI


# Bind declarative base to the DB
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_recycle=3600)
Base.metadata.bind = engine

# A db session object we use across our application
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
