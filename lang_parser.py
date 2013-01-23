"""
Notes while devving:
So this works, gives a table with all words, tags and transformed words):

from pattern.nl import *
pprint(parse(t, lemmata=True, tags=False))

This converts an entire string to normal form like thing, but discards the word
types:

' '.join([x[-1] for x in parse(t, lemmata=True, tags=False).split()[0]
                 if x[-1] not in string.punctuation])

"""


class LanguageParser():
    """Parses given texts in a set language. It can normalize text and extract
    keywords for it."""

    # TODO (optional): detect language if none given?

    LANG_EN = 'en'
    LANG_NL = 'nl'

    def __init__(self, language, texts=[]):
        if language not in (LANG_EN, LANG_NL):
            raise ValueError("Invalid language: %s" % repr(language))

        self.language = language
        self.texts = []
        self.add_texts(texts)

        # TODO: import stuff to setup everything for given language... or do
        # that in the normalize/extract keyword functions?

    def add_texts(self, texts):
        if isinstance(texts, (list, tuple)):
            self.texts += texts
        elif isinstance(texts, str):
            self.texts += [texts]
        else:
            raise ValueError("Unsupported type: %s of '%s'", str(type(texts)),
                             repr(texts))

    def get_normalized(self):
        return map(self.normalize, self.texts)

    def get_keywords(self):
        return map(self.extract_keywords, self.texts)

    def normalize(self, text):
        # TODO: normalize (singularize, lemma)
        return text.lower()  # placeholder

    def extract_keywords(self, text):
        # TODO: normalize, then select... things (nouns, cardinal numbers, ...)
        return text.split()[:-1]  # placeholder
