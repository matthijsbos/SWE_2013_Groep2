import unittest
import sqlalchemy.orm.exc as alchexc
from models.answer import AnswerModel
from dbconnection import session
import os

class BaseUnittest(unittest.TestCase):
    #do not change method names as tests are executed in alphabetical order

    # test basemodel methods
    def test_1get_all(self):
        AnswerModel.save(100,1234,'TEST')
        obj = None
        try:
            obj = AnswerModel().get_all()
        except:
            pass
        self.assertTrue(obj is not None) 

    def test_2by_id(self):
        obj = None
        try:
            obj = AnswerModel().by_id(1)
        except:
            pass
        self.assertTrue(obj is not None) 

    def test_3by_ids(self):
        AnswerModel.save(101,1234,'TEST')
        ids = [1, 2]
        obj = None
        try:
            obj = AnswerModel().by_ids(ids)
        except:
            pass
        self.assertTrue(obj is not None) 
        
    def test_4remove_by_id(self):
        AnswerModel.remove_by_id(1)
        obj = None
        try:
            obj = session.query(AnswerModel).filter_by(id=1).one()
        except:
            pass
        self.assertTrue(obj is None)

    def test_5get_filtered(self):
        obj = None
        try:
            obj = AnswerModel().get_filtered()
        except:
            pass
        self.assertTrue(obj is not None)
        
        obj = None
        try:
            obj = AnswerModel().get_filtered(id = 2)
        except:
            pass
        self.assertTrue(obj is not None)
        

        
if __name__ == '__main__':
    unittest.main()
