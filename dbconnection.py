from sqlalchemy import  *
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

