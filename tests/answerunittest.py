import unittest
import sqlalchemy.orm.exc as alchexc
from models.answer import AnswerModel
#from basemodels.basemodel import BaseEntity
from dbconnection import session
import os

class AnswerUnittest(unittest.TestCase):

    # answer model tests, do not change name as tests are executed in alphabetical order
    def test_1empty(self):
        with self.assertRaises(alchexc.NoResultFound):
            session.query(AnswerModel).filter_by(questionID=101,userID=1234).one()

    def test_2save(self):
        AnswerModel.save(101,1234,'TEST')
        obj = None
        try:
            obj = session.query(AnswerModel).filter_by(questionID=101,userID=1234).one()
        except:
            pass
        self.assertTrue(obj is not None)

    def test_3savereview(self):
        AnswerModel.savereview(999,9999,'TEST',1)
        obj = None
        try:
            obj = session.query(AnswerModel).filter_by(questionID=999,userID=9999).one()
        except:
            pass
        self.assertTrue(obj is not None)

    def test_4updateAnswer(self):
        AnswerModel.updateAnswer(1,'NEW')
        obj = None
        try:
            obj = session.query(AnswerModel).filter_by(id=1,text="NEW").one()
        except:
            pass
        self.assertTrue(obj is not None)
 
    def test_5getAnswerID(self):
        id = None
        try:
            id = AnswerModel.getAnswerID(1234,101)
        except:
            pass
        self.assertTrue(id is not None)
    
    def test_6checkAnswerExist(self):
        bool = None
        try:
            bool = AnswerModel.checkAnswerExist(1234,101)
        except:
            pass
        self.assertTrue(bool is 1)

    def test_7getTimeStamp(self):
        date = None
        try:
            date = AnswerModel.getTimeStamp(1)
        except:
            pass
        self.assertTrue(date is not None)
        
    #def testFilter(self):
    #def testDelete(self):  
    
if __name__ == '__main__':
    unittest.main()
