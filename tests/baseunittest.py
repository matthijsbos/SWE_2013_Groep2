import unittest
import sqlalchemy.orm.exc as alchexc
from models.basemodel import BaseEntity
from models.answer import AnswerModel
from dbconnection import session
import os

class BaseUnittest(unittest.TestCase):
    #do not change method names as tests are executed in alphabetical order

    # test basemodel methods
    def test_1get_all(self):
    #    AnswerModel.save(102,1234,'TEST')
    #    obj = None
    #    try:
    #        obj = BaseEntity.get_all(AnswerModel)
    #    except:
    #        pass
    #    self.assertTrue(obj is not None)
        obj = BaseEntity.derp()
        try:
            obj = BaseEntity.derp()
        except:
            pass
        self.assertTrue(obj is 2)   


if __name__ == '__main__':
    unittest.main()
