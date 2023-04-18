import spacy
import json
import os
import soundex
from gtts import gTTS
import random

class NLP:
    def __init__(self):

        self.nlp = spacy.load('en_core_web_sm')
        self.text = ""
        self.path = os.path.join(os.getcwd(),"../data")
        self.phrases_match = {}
        self.phrases_response = {}
        self.keywords = []
        self.found_matches = []



    def load_dict(self):

        path = os.path.join(self.path,"match")
        for i in os.listdir(path):
            with open(os.path.join(path,i)) as jsonfile:
                temp = json.load(jsonfile)
                self.phrases_match["".join(temp.keys())] = list(temp.values())[0]

        path = os.path.join(self.path, "response")
        for i in os.listdir(path):
            with open(os.path.join(path,i)) as jsonfile:
                temp = json.load(jsonfile)
                self.phrases_response["".join(temp.keys())] = list(temp.values())[0]


    def getKeys(self, text):
        self.text = text.lower()
        doc = self.nlp(self.text)
        self.keywords = []
        self.found_matches = []

        for token in doc:
            if token.pos_ in ['VERB', 'NOUN', 'ADJ', 'INTJ'] and not token.is_stop:
                self.keywords.append(token.text)



        self.check_for_match()

    def check_for_match(self):
        s = soundex.getInstance()

        for word in self.keywords:
            for phrase in self.phrases_match:
                for match in self.phrases_match[phrase]:
                    if s.soundex(match) == s.soundex(word):
                        self.found_matches.append(phrase)

        self.found_matches = list(set(self.found_matches))
        print(f"Scanned words: {self.keywords}")
        print(f"Found matches: {self.found_matches}")

        if self.found_matches.count("yes_match") >= 1 and self.found_matches.count("no_match") < 1:
            if self.found_matches.count("welcome_match") < 1:
                tts = gTTS(text=random.choice(self.phrases_response["pour_match"]), lang='en')
                tts.save("say_file.mp3")
                os.system("start say_file.mp3")

        elif self.found_matches.count("yes_match") < 1 and self.found_matches.count("no_match") < 1:
            if self.found_matches.count("welcome_match") >= 1:
                tts = gTTS(text=random.choice(self.phrases_response["welcome_response"]), lang='en')
                tts.save("say_file.mp3")
                os.system("start say_file.mp3")

        else:
            tts = gTTS(text=random.choice(self.phrases_response["repeat_response"]), lang='en')
            tts.save("say_file.mp3")
            os.system("start say_file.mp3")








