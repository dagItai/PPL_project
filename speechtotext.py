# Import libraries
from __future__ import division
import re
import sys
from threading import Thread
import threading
import beepy
from google.cloud import speech
from microphone_stream import MicrophoneStream
from word_processing import English
import Utils
import os

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="speechRecognition-f76ec204b30b.json"

class speechToText(Thread):
    def __init__(self, *args, **kwargs):
        arg_to_pass = tuple()
        super(speechToText, self).__init__(*arg_to_pass, **kwargs)
        self._stop = threading.Event()
        self.set_params(*args)
        self.client = speech.SpeechClient()

        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.RATE,
            language_code=self.language_code)

        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True)


    def stop(self):
        print("stop")
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.start_speech_to_text()

    def set_params(self,words_list, sound_type, synonyms, write_to_log):
        # Audio recording parameters
        self.RATE = 16000
        self.CHUNK = int(RATE / 10)  # 100ms
        self.language_code = "en-us"
        self.word_processor = English()
        # Params
        self.beep_name = sound_type
        if synonyms:
            self.explicit_words = "|".join(self.word_processor.add_synonyms(words_list))
        else:
            self.explicit_words ="|".join(words_list)
        self.explicit_words = r'\b({})\b'.format(self.explicit_words)
        self.write_to_log = write_to_log



    def listen_print_loop(self, responses):
        """Iterates through server responses and prints them.

        The responses passed is a generator that will block until a response
        is provided by the server.

        Each response may contain multiple results, and each result may contain
        multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
        print only the transcription for the top alternative of the top result.

        In this case, responses are provided for interim results as well. If the
        response is an interim one, print a line feed at the end of it, to allow
        the next result to overwrite it, until the response is a final one. For the
        final one, print a newline to preserve the finalized transcription.
        """
        num_chars_printed = 0
        for response in responses:
            if self.stopped():
                print("return stop")
                return
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                print(transcript + overwrite_chars)

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(self.explicit_words, transcript, re.I):
                    # What to do when you hear the explicit word
                    Utils.play_beep(self.beep_name)
                    if self.write_to_log:
                        Utils.write_to_log(transcript)
                num_chars_printed = 0

    def start_speech_to_text(self):
        with MicrophoneStream(self.RATE, self.CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)
            print("Start talking....")
            responses = self.client.streaming_recognize(self.streaming_config, requests)


            # Now, put the transcription responses to use.
            self.listen_print_loop(responses)


