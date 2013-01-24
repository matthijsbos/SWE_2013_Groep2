# ldig integration into e-learning environment
#
# Based on ldig server released under MIT License.
# (c)2011 Nakatani Shuo / Cybozu Labs Inc.
#
# Author: Arjen Tamerus

import ldig
import numpy

class Ldig_parser():

    def __init__(self, model_dir):
        self.ldig = ldig.ldig(model_dir)
        self.features = self.ldig.load_features()
        self.trie = self.ldig.load_da()
        self.labels = self.ldig.load_labels()
        self.param = numpy.load(self.ldig.param)

    def parse_answer(self, answer):
        _, text, _ = ldig.normalize_text(answer)
        events = self.trie.extract_features(u"\u0001" + answer + u"\0001")
        sum = numpy.zeros(len(self.labels))

        data = []
        for id in sorted(events, key=lambda id:self.features[id][0]):
            phi = self.param[id,]
            sum += phi * events[id]
        exp_w = numpy.exp(sum - sum.max())
        prob = exp_w / exp_w.sum()
        return [x for x in prob]

    def parse_answers(self, answers):
        #if isinstance(answers, str):
        #    answers = [answers]
        #print answers
        #if type(answers) == "string"
        answer_lang = numpy.zeros(len(self.labels))
        for i in range(3 if len(answers) > 2 else len(answers)):
            answer_lang += self.parse_answer(answers[i])
        answer_lang = answer_lang / answer_lang.sum()

        lang_max = -1
        lang_maxval = -1
        i = 0
        for lang in answer_lang:
            if lang > lang_maxval:
                lang_max = i
                lang_maxval = lang
            i += 1

        #print answer_lang[lang_max]

        if answer_lang[lang_max] > 0.6:
            return self.labels[lang_max]

        return '00'

if __name__ == "__main__":
    parser = Ldig_parser("ldig_model.small")
    print parser.parse_answers(["I am an engineer.","As are you!","How nice,isn't it?"])
    print parser.parse_answers(["Ik ben gek"])
    print parser.parse_answers(["Ik ben Arjen Tamerus"])
    print parser.parse_answers(["Ik ben Arjen Tamerus", "Hola espanola"])
