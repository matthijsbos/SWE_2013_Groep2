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

import string

class LanguageParser():
    """Parses given texts in a set language. It can normalize text and extract
    keywords for it."""

    # TODO (optional): detect language if none given?

    LANG_EN = 'en'
    LANG_NL = 'nl'

    def __init__(self, language, texts=[]):
        if language not in (self.LANG_EN, self.LANG_NL):
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
        if self.language == self.LANG_EN:
            from pattern.en import parse
        elif self.language == self.LANG_NL:
            from pattern.nl import parse
        else:
            raise Exception("Unsupported language: %s" % repr(self.language))

        parsed = parse(text, lemmata=True, chunks=False)
        print parsed
        t = []
        for x in parsed.split():
            t += x
        print t
        t = [x[-1] for x in t if x[-1] not in string.punctuation]
        t = ' '.join(t)

        return t

    def extract_keywords(self, text):
        keyword_types = ('NN', 'NNS', 'NNP', 'NNPS', 'CD', 'FW')
        keyword_types_fallback = ('VBZ', 'VBP', 'VBD', 'VBN', 'VBG')

        if self.language == self.LANG_EN:
            from pattern.en import parse, pprint
        elif self.language == self.LANG_NL:
            from pattern.nl import parse, pprint
        else:
            raise Exception("Unsupported language: %s" % repr(self.language))

        parsed = parse(text, lemmata=True, chunks=False)
        pprint(parsed)

        parsed = [x for y in parsed.split() for x in y]  # Flatten
        parsed = filter(lambda w: w[-1] not in string.punctuation, parsed)
        keywords = filter(lambda w: w[1] in keyword_types, parsed)
        if not keywords:
            keywords = filter(lambda w: w[1] in keyword_types_fallback, parsed)
        if not keywords:
            keywords = parsed
        keywords = map(lambda w: w[-1], keywords)

        return keywords
