from sqlalchemy import  *
from sqlalchemy import exc as exc
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

