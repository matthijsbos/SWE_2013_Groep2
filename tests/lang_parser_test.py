import unittest

from dbconnection import session
import lang_parser
#from .. import lang_parser

class TestLanguageParser(unittest.TestCase):
    def test_normalize_en(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('en')

        eq(p.normalize("This is a test."), "this be a test")
        eq(p.normalize("There is a box in the boxes."),
                       "there be a box in the box")
        eq(p.normalize("Martin Luthor King Jr. was killed in 1968."),
                       "martin luthor king jr. be kill in 1968")
        eq(p.normalize("That is my ex-wife."), "that be my ex-wife")

    def test_keywords_en(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('en')

        eq(set(p.extract_keywords("This is a test.")), set(["test"]))
        eq(set(p.extract_keywords("There is a box in the boxes.")),
                set(["box"]))
        eq(set(p.extract_keywords("Martin Luthor King Jr. was killed in " +
            "1968.")), set(["martin", "luthor", "king", "jr.", "1968"]))
        eq(set(p.extract_keywords("That is my ex-wife.")), set(["ex-wife"]))
    
    def test_normalize_nl(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('nl')

        eq(p.normalize("Dit is een test."), "dit zijn een test")
        eq(p.normalize("Er is een veld in de velden."),
                       "er zijn een veld in de veld")
        eq(p.normalize("Martin Luthor King Jr. was vermoord in 1968."),
                       "martin luthor king jr. zijn vermoorden in 1968")
        eq(p.normalize("Dat is mijn ex-vrouw."), "dat zijn mijn ex-vrouw")

    def test_keywords_nl(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('nl')

        eq(set(p.extract_keywords("Dit is een test.")), set(["test"]))
        eq(set(p.extract_keywords("Er is een veld in de velden.")), set(["veld"]))
        eq(set(p.extract_keywords("Martin Luthor King Jr. was vermoord in " +
            "1968.")), set(["martin", "luthor", "king", "jr.", "1968"]))
        eq(set(p.extract_keywords("Dat is mijn ex-vrouw.")), set(["ex-vrouw"]))

    def test_normalize_de(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('de')

        eq(p.normalize("Dies ist ein Test."), "die sein ein test")
        eq(p.normalize("Gibt es ein Box in den boxen."),
                       "geben es ein box in den boxen")
        eq(p.normalize("Martin Luthor King Jr. wurde 1968 ermordet."),
                       "martin luthor king jr. werden 1968 ermordet")
        eq(p.normalize("Dies ist meine Ex-Frau."), "die sein meine ex-frau")

    def test_keywords_de(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('de')

        eq(set(p.extract_keywords("ies ist ein Test.")), set(["test"]))
        eq(set(p.extract_keywords("Gibt es ein box in den boxen.")), set(["box", "boxen"]))
        eq(set(p.extract_keywords("Martin Luthor King Jr. wurde 1968 ermordet.")),                               set(["luthor", "king", "jr.", "1968", "ermordet"]))
        eq(set(p.extract_keywords("Dies ist meine Ex-Frau.")), set(["ex-frau"]))

    def test_normalize_es(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('es')

        eq(p.normalize("Esto es una prueba."), "esto ser un prueba")
        eq(p.normalize("Hay una caja en las cajas."),
                       "haber un caja en el caja")
        eq(p.normalize("Martin Luthor King Jr. fue asesinado en 1968."),
                       "martin luthor king jr. ir asesinar en 1968")
        eq(p.normalize("Esta es mi ex exposa."), "esta ser mi ex exposo")

    def test_keywords_es(self):
        eq = self.assertEqual
        p = lang_parser.LanguageParser('es')

        eq(set(p.extract_keywords("Esto es una prueba.")), set(["prueba"]))
        eq(set(p.extract_keywords("Hay una caja en las cajas.")), set(["caja"]))
        eq(set(p.extract_keywords("Martin Luthor King Jr. fue asesinado en 1968.")), set(["martin", "luthor", "king", "jr.", "1968"]))
        eq(set(p.extract_keywords("Esta es mi ex exposa.")), set(["exposo", "ex"]))




if __name__ == '__main__':
    unittest.main()
