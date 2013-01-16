from models import answers
from flask import render_template
from dbconnection import engine, session

Base = declarative_base()

class Rating(Base):
	__tablename__ = 'Ratings'
	
	id = Column(Integer, Sequence('id'), primary_key=True, unique=True)
	rating = Column(Integer)
	userID = Column(Integer)
	
	def __init__(self, rating, userID):
		self.rating = rating
		self.userID = userID
		
	@staticmethod
	def submit_rating(rating):
		session.add(Ratings(rating))
		session.commit()
		
class AnswerRating(Base):
	__tablename__ = 'AwnserRatings'
	
	answer_id = Column(Integer, ForeignKey('answer.id'), primary_key=True)
	rating_id = Column(Integer, ForeignKey('Ratings.id'), primary_key=True)
	
	def __init__(self, answer_id, rating_id):
        self.answer_id = answer_id
        self.rating_id = rating_id
		
	def __repr__(self):
        return "<AnswerRating('%d', '%d')>" % (self.answer_id, self.rating_id)
		
		
Base.metadata.create_all(engine)