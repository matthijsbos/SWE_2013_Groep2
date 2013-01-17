import unittest
from dbconnection import Base,engine
from os import name, path, rename, getcwd,remove




class AnswerUnittest(unittest.TestCase):
    
    directory_separator = ('/' if name == "posix" else '\\')
    #src = getcwd()+directory_separator+"db.sqlite"
    #dst = getcwd()+directory_separator+"db_backup.sqlite"
    #rename(src, dst)
    def setUp(self):
        # backup db file
        src = getcwd()+directory_separator+"db.sqlite"
        dst = getcwd()+directory_separator+"db_backup.sqlite"
        rename(src, dst)
    
        #setup db again
        #Base.metadata.create_all(engine)

    #def tearDown(self):
        #close db connection
    #    Base.metadata.drop_all(engine)
        
        #restore backup 'production'
    #    dst = getcwd()+directory_separator+"db.sqlite"
    #    src = getcwd()+directory_separator+"db_backup.sqlite"
    #    remove(dst)
    #    rename(src, dst)
    
    #def testInsert(self):
    #    session.add(AnswerModel(
    #        questionID=1, userID=1, text="1", edit=0))
    #    session.commit()
    #assert.isTrue(
    #def testFilter(self):
    #def testDelete(self):  
    
if __name__ == '__main__':
    unittest.main()