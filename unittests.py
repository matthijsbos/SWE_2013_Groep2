import unittest
import models
import os
from dbconnection import Base, engine, session
from tests.answerunittest import AnswerUnittest
from tests.baseunittest import BaseUnittest
from tests.lang_parser_test import TestLanguageParser


directory_separator = ('/' if os.name == "posix" else '\\')

def setUp():
    # backup db file
    src = os.getcwd()+directory_separator+"db.sqlite"
    dst = os.getcwd()+directory_separator+"db_backup.sqlite"
    if os.path.exists(src):
        os.rename(src, dst)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    #setup db again

def tearDown():
    #close db connection
    session.expunge_all()
    session.commit()
    session.flush()
    Base.metadata.drop_all(engine)

    #restore backup 'production'
    dst = os.getcwd()+directory_separator+"db.sqlite"
    src = os.getcwd()+directory_separator+"db_backup.sqlite"
    if os.path.exists(dst):
        os.remove(dst)
        if os.path.exists(src):
            os.rename(src, dst)

if __name__ == '__main__':
    # tests dont take eachother in account, for now just rebuild the db for each test

    base_test = unittest.TestLoader().loadTestsFromTestCase(BaseUnittest)
    answer_test = unittest.TestLoader().loadTestsFromTestCase(AnswerUnittest)
    lang_parser_test = \
            unittest.TestLoader().loadTestsFromTestCase(TestLanguageParser)

    setUp()
    unittest.TextTestRunner(verbosity=2).run(answer_test)
    tearDown()

    setUp()
    unittest.TextTestRunner(verbosity=2).run(base_test)
    tearDown()

    setUp()
    unittest.TextTestRunner(verbosity=2).run(base_test)
    tearDown()

    setUp()
    unittest.TextTestRunner(verbosity=2).run(answer_test)
    tearDown()

    unittest.TextTestRunner(verbosity=2).run(lang_parser_test)
