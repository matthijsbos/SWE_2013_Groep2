import unittest

from dbconnection import session
import lang_parser
#from .. import lang_parser

class TestLanguageParser(unittest.TestCase):
    def test_normalize(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('en')

        eq(p.normalize("This is a test."), "this be a test")
        eq(p.normalize("There is a box in the boxes."),
                       "there be a box in the box")
        eq(p.normalize("Martin Luthor King Jr. was killed in 1968."),
                       "martin luthor king jr. be kill in 1968")
        eq(p.normalize("That is my ex-wife."), "that be my ex-wife")

    def test_keywords(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('en')

        eq(set(p.extract_keywords("This is a test.")), set(["test"]))
        eq(set(p.extract_keywords("There is a box in the boxes.")),
                set(["box"]))
        eq(set(p.extract_keywords("Martin Luthor King Jr. was killed in " +
            "1968.")), set(["martin", "luthor", "king", "jr.", "1968"]))
        eq(set(p.extract_keywords("That is my ex-wife.")), set(["ex-wife"]))



if __name__ == '__main__':
    unittest.main()
