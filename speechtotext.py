# Import libraries
from __future__ import division
import re
import sys

import beepy
from google.cloud import speech
from microphone_stream import MicrophoneStream
from word_processing import English
import Utils
# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Params
explicit_words = r'\b(מטלה|מייל|בית ספר)\b'
synonym_words = r'\b(שיעור|מייל|עבודה)\b'

class speechToText:
    def __init__(self):
        # Audio recording parameters
        self.RATE = 16000
        self.CHUNK = int(RATE / 10)  # 100ms

        self.language_code = "en-us"
        self.word_processor = English()
        # Params
        self.beep_name = sound_type
        if synonyms:
            self.explicit_words = self.word_processor.add_synonyms(words_list)
        else:
            self.explicit_words = words_list
        self.write_to_log = write_to_log

    def set_params(self,words_list, sound_type, synonyms, write_to_log):

        self.language_code = "en-us"
        self.word_processor = English()
        # Params
        self.beep_name = sound_type
        if synonyms:
            self.explicit_words = self.word_processor.add_synonyms(words_list)
        else:
            self.explicit_words = words_list
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

                    print("1\n")
                num_chars_printed = 0

    def start_speech_to_text(self):
        client = speech.SpeechClient()

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.RATE,
            language_code=self.language_code)

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        with MicrophoneStream(self.RATE, self.CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            print("Start talking....")
            # Now, put the transcription responses to use.
            self.listen_print_loop(responses)


