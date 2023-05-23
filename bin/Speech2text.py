
import re
import sys
import time
import os

from google.cloud import speech
from Microphone import ResumableMicrophoneStream
from NLP import NLP as nlp

import threading

# Audio recording parameters
STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"


class Speech2text:

    def __init__(self, nlp):
        self.nlp = nlp
        self.start_time = 0

    def get_current_time(self):
        return int(round(time.time() * 1000))




    def listen_print_loop(self,responses, stream):

        """
        Get chunks of audio from microphone.generator and sends them to google Speech to Text
        """

        interpreter = self.nlp
        for response in responses:

            if self.get_current_time() - stream.start_time > STREAMING_LIMIT:
                stream.start_time = self.get_current_time()
                break

            if not response.results:
                continue

            result = response.results[0]

            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript

            result_seconds = 0
            result_micros = 0

            if result.result_end_time.seconds:
                result_seconds = result.result_end_time.seconds

            if result.result_end_time.microseconds:
                result_micros = result.result_end_time.microseconds

            stream.result_end_time = int((result_seconds * 1000) + (result_micros / 1000))

            corrected_time = (
                stream.result_end_time
                - stream.bridging_offset
                + (STREAMING_LIMIT * stream.restart_counter)
            )

            if result.is_final:

                sys.stdout.write(GREEN)
                sys.stdout.write("\033[K")
                sys.stdout.write(str(corrected_time) + ": " + transcript + "\n")
                
                t = threading.Thread(target = interpreter.getKeys, args=(transcript,))
                t.start()


                stream.is_final_end_time = stream.result_end_time
                stream.last_transcript_was_final = True

                # Check for terminating command
                if re.search(r"\b(exit|quit)\b", transcript, re.I):
                    sys.stdout.write(YELLOW)
                    sys.stdout.write("Exiting...\n")
                    stream.closed = True
                    break

                t = threading.Thread(target=interpreter.getKeys(transcript), args=(transcript,))
                t.start()
                sys.stdout.write(str(result_micros))

            else:
                sys.stdout.write(RED)
                sys.stdout.write("\033[K")
                sys.stdout.write(str(corrected_time) + ": " + transcript + "\r")

                stream.last_transcript_was_final = False






    def Start(self):

        """
        Handles connection to google-cloud
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
        client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=SAMPLE_RATE,
            language_code="en-US",
            max_alternatives=1,
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config, interim_results=True
        )

        mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)
        print(mic_manager.chunk_size)
        sys.stdout.write(YELLOW)
        sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')
        sys.stdout.write("End (ms)       Transcript Results/Status\n")
        sys.stdout.write("=====================================================\n")


        with mic_manager as stream:

            while not stream.closed:
                sys.stdout.write(YELLOW)
                sys.stdout.write(
                    "\n" + str(STREAMING_LIMIT * stream.restart_counter) + ": NEW REQUEST\n"
                )
                

                stream.audio_input = []
                audio_generator = stream.generator()

                requests = (
                    speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator
                )

                responses = client.streaming_recognize(streaming_config, requests)


                self.listen_print_loop(responses, stream)

                if stream.result_end_time > 0:
                    stream.final_request_end_time = stream.is_final_end_time
                stream.result_end_time = 0
                stream.last_audio_input = []
                stream.last_audio_input = stream.audio_input
                stream.audio_input = []
                stream.restart_counter = stream.restart_counter + 1

                if not stream.last_transcript_was_final:
                    sys.stdout.write("\n")
                stream.new_stream = True


