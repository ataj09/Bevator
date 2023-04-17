import spacy
import json

class NLP:
    def __init__(self):
        import spacy
        self.nlp = spacy.load('en_core_web_sm')
        self.text = ""

    def getKeys(self, text):
        self.text = text.lower()
        doc = self.nlp(self.text)
        keywords = []

        for token in doc:
            if token.pos_ in ['VERB','NOUN'] and not token.is_stop:
                keywords.append(token.text)
        print(keywords)

