import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.environ["SQLALCHEMY_DATABASE_URI"])

Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
