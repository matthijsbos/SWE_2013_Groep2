import unittest
import models
import os
from dbconnection import Base, engine
from tests.answerunittest import AnswerUnittest


directory_separator = ('/' if os.name == "posix" else '\\')

def setUp():
    # backup db file
    print "hello test"
    src = os.getcwd()+directory_separator+"db.sqlite"
    dst = os.getcwd()+directory_separator+"db_backup.sqlite"
    if os.path.exists(src):
        os.rename(src, dst)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    #setup db again

def tearDown():
    #close db connection
    Base.metadata.drop_all(engine)
    
    #restore backup 'production'
    dst = os.getcwd()+directory_separator+"db.sqlite"
    src = os.getcwd()+directory_separator+"db_backup.sqlite"
    if os.path.exists(dst):
        os.remove(dst)
        if os.path.exists(src):
            os.rename(src, dst)

if __name__ == '__main__':

    setUp()
    suite = unittest.TestLoader().loadTestsFromTestCase(AnswerUnittest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    tearDown()

