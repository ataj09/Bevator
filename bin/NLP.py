import spacy
import json
import os
import soundex

class NLP:
    def __init__(self):
        import spacy
        self.nlp = spacy.load('en_core_web_sm')
        self.text = ""
        self.path = os.path.join(os.getcwd(),"../data")
        self.phrases = {}
        self.keywords = []
        self.found_matches = []


    def load_dict(self):

        for i in os.listdir(self.path):
            with open(os.path.join(self.path,i)) as jsonfile:
                temp = json.load(jsonfile)
                self.phrases["".join(temp.keys())] = list(temp.values())[0]

    def getKeys(self, text):
        self.text = text.lower()
        doc = self.nlp(self.text)
        self.keywords = []
        self.found_matches = []

        for token in doc:
            if token.pos_ in ['VERB','NOUN'] and not token.is_stop:
                self.keywords.append(token.text)


        self.check_for_match()

    def check_for_match(self):
        s = soundex.getInstance()

        for word in self.keywords:
            for phrase in self.phrases:
                for match in self.phrases[phrase]:
                    if s.soundex(match) == s.soundex(word):
                        self.found_matches.append(phrase)

        self.found_matches = list(set(self.found_matches))
        print(f"Scanned words: {self.keywords}")
        print(f"Found matches: {self.found_matches}")


