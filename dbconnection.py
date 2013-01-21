from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc as exc
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.sqlite',
        connect_args={'check_same_thread':False})
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base = declarative_base()
