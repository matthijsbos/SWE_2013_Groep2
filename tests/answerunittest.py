import unittest
import sqlalchemy.orm.exc as alchexc
from models.answer import AnswerModel
from dbconnection import session
import os

class AnswerUnittest(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(alchexc.NoResultFound):
            session.query(AnswerModel).filter_by(questionID=101,userID=1234).one()

    def test_insert(self):
        AnswerModel.save(101,1234,'TEST')
        obj = None

        try:
            obj = session.query(AnswerModel).filter_by(questionID=101,userID=1234).one()
        except:
            pass
        self.assertTrue(obj is not None)

    #def testFilter(self):
    #def testDelete(self):  
    
if __name__ == '__main__':
    unittest.main()
