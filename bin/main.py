import threading
import Speech2text
import NLP

def main():
    nlp = NLP.NLP()
    nlp.load_dict()
    s2t = Speech2text.Speech2text(nlp)
    t1 = threading.Thread(s2t.Start())
    t1.start()



if __name__ == "__main__":
    main()