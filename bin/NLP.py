import spacy
import json
import os

class NLP:
    def __init__(self):
        import spacy
        self.nlp = spacy.load('en_core_web_sm')
        self.text = ""
        self.path = os.path.join(os.getcwd(),"../data")
        self.phrases = {}

    def load_dict(self):

        for i in os.listdir(self.path):
            with open(i) as jsonfile:
                temp = json.load(jsonfile)

    def getKeys(self, text):
        self.text = text.lower()
        doc = self.nlp(self.text)
        keywords = []

        for token in doc:
            if token.pos_ in ['VERB','NOUN'] and not token.is_stop:
                keywords.append(token.text)
        print(keywords)

