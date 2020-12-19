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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="speechRecognition-76fe4cfdf56d.json"

class speechToText(Thread):
    '''
    This class responsible for the speech-to-text process and finding the given word in the text
    Extending the Thread Class
    '''
    def __init__(self, *args, **kwargs):
        '''
        Initializes the class with super (Thread) and setting all the given parameters for later use
        Args:
            *args: the args that needed to set parameters for this class
            **kwargs: needed for pass to super
        '''

        arg_to_pass = tuple() #for passs to super
        super(speechToText, self).__init__(*arg_to_pass, **kwargs)
        self._stop = threading.Event()
        self.set_params(*args)
        self.set_speech()

    def stop(self):
        '''
        Extending the Thread Class
        '''
        self._stop.set()

    def stopped(self):
        '''
        Extending the Thread Class
        '''
        return self._stop.isSet()

    def run(self):
        '''
        Extending the Thread Class - will run on start()
        '''
        self.start_speech_to_text()

    def set_params(self, words_list, sound_type, synonyms, write_to_log):
        '''
        setting the variables ans the parameters that will be needed for set_speech and listen_loop
        Args:
            words_list: the given word by the user
            sound_type: the chosen sound type by the user
            synonyms: true or false, set by the user
            write_to_log: true or false, set by the user
        '''
        # Audio recording parameters
        self.RATE = 16000
        self.CHUNK = int(self.RATE / 10)  # 100ms
        # Language parameter
        self.language_code = "en-us"
        self.word_processor = English()
        # Sound parameter
        self.beep_name = sound_type
        # Use the word_processor if synonyms true to find synonyms for all the words in words_list
        words_list = self.word_processor.stem_keywrod_list(words_list)
        if synonyms:
            self.explicit_words = "|".join(self.word_processor.add_synonyms(words_list))
        else:
            self.explicit_words ="|".join(words_list)
        # Create regex from all the words
        self.explicit_words = r'\b({})\b'.format(self.explicit_words)
        print(self.explicit_words)
        # Set write to log
        self.write_to_log = write_to_log

    def set_speech(self):
        '''
        Set the variables that needed for streaming_recognize
        '''
        self.client = speech.SpeechClient()

        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.RATE,
            language_code=self.language_code)

        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True)


    def listen_loop(self, responses):
        '''
        Iterates through server responses and look for regex. If the regex has been found beep sound will be heard.
        Args:
            responses: generator that will block until a response is provided by the server
        '''

        num_chars_printed = 0
        for response in responses:
            # check that _stop flag raised
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
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                print(transcript + overwrite_chars)
                transcript = self.word_processor.stem_from_voice(transcript)
                print(transcript)
                # Exit recognition if any of the transcribed phrases could be
                # one of keywords that have been given by the user.
                if re.search(self.explicit_words, transcript, re.I):
                    # Beep
                    Utils.play_beep(self.beep_name)
                    # Write to log if the user wanted
                    if self.write_to_log:
                        Utils.write_to_log(transcript)
                num_chars_printed = 0

    def start_speech_to_text(self):
        '''
        Response to open the microphone stream and send it to the API to create from that transcription
        '''
        with MicrophoneStream(self.RATE, self.CHUNK) as stream:
            # In practice, stream should be a generator yielding chunks of audio data
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)
            print("Start talking....")

            # streaming_recognize returns a generator
            responses = self.client.streaming_recognize(self.streaming_config, requests)


            # create transcription from the responses
            self.listen_loop(responses)




