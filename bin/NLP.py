import spacy
import json
import os
import soundex
from gtts import gTTS
import random
import time


class NLP:
    """
    Class responsible for extracting keywords from text and mapping into
    appropriate robot controlling functions

    """

    def __init__(self):

        self.nlp = spacy.load('en_core_web_sm')
        self.text = ""
        self.path = os.path.join(os.getcwd(), "../data")
        self.phrases_match = {}
        self.phrases_response = {}
        self.keywords = []
        self.found_matches = []
        self.listen_flag = -10
        self.listen_time = 30

    def get_current_time(self):
        return int(round(time.time()))

    def load_dict(self):
        """
            Load datasets from directory

        """
        path = os.path.join(self.path, "match")
        for i in os.listdir(path):
            with open(os.path.join(path, i)) as jsonfile:
                temp = json.load(jsonfile)
                self.phrases_match["".join(temp.keys())] = list(temp.values())[0]

        path = os.path.join(self.path, "response")
        for i in os.listdir(path):
            with open(os.path.join(path, i)) as jsonfile:
                temp = json.load(jsonfile)
                self.phrases_response["".join(temp.keys())] = list(temp.values())[0]

    def getKeys(self, text):

        """
        extracting key words from text and calling matcher
        :param text: string with is gonna be processed
        :return: none
        """
        self.text = text.lower()
        doc = self.nlp(self.text)
        self.keywords = []
        self.found_matches = []

        for token in doc:
            if token.pos_ in ['VERB', 'NOUN', 'ADJ', 'INTJ'] and not token.is_stop:
                self.keywords.append(token.text)

        self.check_for_match()

    def check_for_match(self):
        """
        Match keywords with robot controlling functions
        :return:
        """
        s = soundex.getInstance()

        # THIS PART IS GOING TO BE REPLACED WITH SOME SIMPLE CLASSIFYING AI

        for word in self.keywords:
            for phrase in self.phrases_match:
                for match in self.phrases_match[phrase]:
                    if s.soundex(match) == s.soundex(word):
                        self.found_matches.append(phrase)

        self.found_matches = list(set(self.found_matches))
        print(f"Scanned words: {self.keywords}")
        print(f"Found matches: {self.found_matches}")

        if self.found_matches.count("yes_match") < 1 \
                and self.found_matches.count("no_match") < 1 \
                and self.found_matches.count("welcome_match") >= 1\
                and self.get_current_time() - self.listen_flag:
            tts = gTTS(text=random.choice(self.phrases_response["welcome_response"]), lang='en')
            tts.save("say_file.mp3")
            os.system("start say_file.mp3")
            self.listen_flag = self.get_current_time()
            return

            # Begin listening to users other commands

        if self.get_current_time() - self.listen_flag < self.listen_time:

            #other reponses will be generated only when "Bevator" was called in last self.listen_time seconds
            if self.found_matches.count("yes_match") >= 1 \
                    and self.found_matches.count("no_match") < 1 \
                    and self.found_matches.count("welcome_match") < 1:

                tts = gTTS(text=random.choice(self.phrases_response["pour_response"]), lang='en')
                tts.save("say_file.mp3")
                os.system("start say_file.mp3")

                # Call robot siutable functions to pour selected drink


            else:
                tts = gTTS(text=random.choice(self.phrases_response["repeat_response"]), lang='en')
                tts.save("say_file.mp3")
                os.system("start say_file.mp3")
                # Ask for repetition

        else:
            pass
