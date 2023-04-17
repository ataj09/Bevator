import threading
import Speech2text
import NLP

def main():
    nlp = NLP.NLP()
    s2t = Speech2text.Speech2text(nlp)

if __name__ == "__main__":
    main()