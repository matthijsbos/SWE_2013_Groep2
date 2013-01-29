from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from dbconnection import engine, session, Base
from models.answer import AnswerModel
from basemodel import BaseEntity

class Rating(Base):
	__tablename__ = 'Ratings'
	
	id = Column(Integer, Sequence('id'), primary_key=True, unique=True)
	rating = Column(Integer)
	#TODO: ForeignKey
	userID = Column(Integer)
	
	def __init__(self, rating, userID):
		self.rating = rating
		self.userID = userID
	
	@staticmethod
	def get_all():
		return session.query(Rating).filter().all()
	
	@staticmethod
	def submit_rating(rating):
		session.add(Rating(rating))
		session.commit()
		
class AnswerRating(Base):
	__tablename__ = 'AnswerRatings'
	
	answer_id = Column(Integer, ForeignKey('answer.id'), primary_key=True)
	rating_id = Column(Integer, ForeignKey('Ratings.id'), primary_key=True)
	
	def __init__(self, answer_id, rating_id):
		self.answer_id = answer_id
		self.rating_id = rating_id
		
	def __repr__(self):
		return "<AnswerRating('%d', '%d')>" % (self.answer_id, self.rating_id)
		
	@staticmethod
	def get_all():
		return session.query(AnswerRating).filter().all()

	@staticmethod
	def add_answerrating(aid, rid):
		if session.query(AnswerRating).filter(
					AnswerRating.answer_id==aid,
					AnswerRating.rating_id==rid).first() is None:
				session.add(AnswerRating(aid, rid))	
		
