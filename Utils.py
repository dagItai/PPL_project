import os
import datetime
import beepy

# import winsound
# frequency = 2500  # Set Frequency To 2500 Hertz
# duration = 1000  # Set Duration To 1000 ms == 1 second
# winsound.Beep(frequency, duration)
import time
import sys



def play_beep(beep_name):
    beepy.beep(sound=beep_name)

def fetch_input(self):
        '''
        Responsible for get the parameter that the user have been set in the GUI
        :return: 3 parameter that the user set: start_location, trip_duration, recommendations_no
        '''
        # words input
        words_list = self.ids.word.text.split(",")
        words_list = map(str.strip, words_list)
        # sound type
        sound_type = self.ids.sound.text.strip()
        # synonyms
        synonyms = self.ids.synonyms.active
        # write to log
        write_to_log = self.ids.synonyms.active

def write_to_log(sentence):
    full_date = datetime.datetime.now()
    filename = f"{full_date.strftime('%x')}_{full_date.strftime('%X')}_zoom_sentence.txt"

    if os.path.exists(filename):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not

    sentence_file = open(filename, append_write)
    sentence_file.write(f"Time: {full_date}, Sentence: {sentence}'\n'")
    sentence_file.close()



play_beep("aaa")