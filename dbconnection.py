from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()