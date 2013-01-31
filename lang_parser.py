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

    # TODO: detect language if none given?

    LANG_EN = 'en'
    LANG_NL = 'nl'
    LANG_DE = 'de'
    LANG_ES = 'es'
    LANG_UNKNOWN = '00'

    def __init__(self, language = LANG_UNKNOWN, texts = [], detector = None):
        if language not in (self.LANG_EN, self.LANG_NL, self.LANG_DE,
                            self.LANG_ES, self.LANG_UNKNOWN):
            raise ValueError("Invalid language: %s" % repr(language))

        self.texts = []
        self.add_texts(texts)
        self.language = language
        self.lang_detector = detector

    def add_texts(self, texts):
        if isinstance(texts, (list, tuple)):
            self.texts += texts
        elif isinstance(texts, str):
            self.texts += [texts]
        else:
            raise ValueError("Unsupported type: %s of '%s'", str(type(texts)),
                             repr(texts))

    def get_normalized(self):
        self.detect_language()
        return map(self.normalize, self.texts)

    def get_keywords(self):
        self.detect_language()
        return map(self.extract_keywords, self.texts)

    def normalize(self, text):
        """Normalizes a given string by:
            * singularizing any plurals.
            * getting the base form of any verb
            * eliminating all capitals"""

        if self.language == self.LANG_EN:
            from pattern.en import parse
        elif self.language == self.LANG_NL:
            from pattern.nl import parse
        elif self.language == self.LANG_DE:
            from pattern.de import parse
        elif self.language == self.LANG_ES:
            from pattern.es import parse
        elif self.language == self.LANG_UNKNOWN:
            # Don't do any parsing.
            return text.lower()
        else:
            raise Exception("Unsupported language: %s" % repr(self.language))

        parsed = parse(text, lemmata=True, chunks=False)
        parsed = [x for y in parsed.split() for x in y]  # Flatten
        normalized = map(lambda w: w[-1], parsed)
        normalized = filter(lambda w: w not in string.punctuation, normalized)
        normalized = ' '.join(normalized)
        return normalized

    def extract_keywords(self, text):
        """Extracts keywords from a given string.

        The string is first analysed and normalized. First, it tries to find
        any nouns, cardinal number or foreign words.
        If that set is empty, all verbs are returned.
        If even that set is empty, every word in the sentence is returned as
        keyword."""

        keyword_types = ('NN', 'NNS', 'NNP', 'NNPS', 'CD', 'FW')
        keyword_types_fallback = ('VBZ', 'VBP', 'VBD', 'VBN', 'VBG', 'JJ', 'JJS', 'JJR')

        if self.language == self.LANG_EN:
            from pattern.en import parse
        elif self.language == self.LANG_NL:
            from pattern.nl import parse
        elif self.language == self.LANG_DE:
            from pattern.de import parse
        elif self.language == self.LANG_ES:
            from pattern.es import parse
        elif self.language == self.LANG_UNKNOWN:
            # Don't do any language parsing depending on a specific language.
            return text.lower().translate(string.maketrans("", ""),
                                          string.punctuation).split()
        else:
            raise Exception("Unsupported language: %s" % repr(self.language))

        parsed = parse(text, lemmata=True, chunks=False)
        parsed = [x for y in parsed.split() for x in y]  # Flatten
        parsed = filter(lambda w: w[-1] not in string.punctuation, parsed)
        keywords = filter(lambda w: w[1] in keyword_types, parsed)
        if not keywords:
            keywords = filter(lambda w: w[1] in keyword_types_fallback, parsed)
        if not keywords:
            keywords = parsed
        keywords = map(lambda w: w[-1], keywords)
        keywords = {}.fromkeys(keywords).keys()
        return keywords

    def detect_language(self):
        if self.lang_detector:
            self.language = self.lang_detector.parse_answers(texts)
