
import threading
import NLP
import Speech2text
import motor

def main():
    """
    Runs whole control system
    1: Load text dictonaries
    2: Start listening to microphone on new thread
    3: Start robot control on new thread
    """


    robot_system = motor.Motor()
    t2 = threading.Thread(target=robot_system.start)
    t2.start()

    nlp = NLP.NLP(motor)
    nlp.load_dict()

    s2t = Speech2text.Speech2text(nlp)
    t1 = threading.Thread(target= s2t.Start)
    t1.start()



if __name__ == "__main__":
    main()
