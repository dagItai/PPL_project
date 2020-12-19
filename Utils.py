import os
import datetime
import beepy

# import winsound
# frequency = 2500  # Set Frequency To 2500 Hertz
# duration = 1000  # Set Duration To 1000 ms == 1 second
# winsound.Beep(frequency, duration)
import time
import sys

full_date = datetime.datetime.now()

def play_beep(beep_name):
    beepy.beep(sound=beep_name)

def write_to_log(sentence):
    filename = f"{full_date.strftime('%d%m%y')}_{full_date.strftime('%H%M%S')}_zoom_sentence.txt"

    if os.path.exists(filename):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not

    sentence_file = open(filename, append_write)
    sentence_file.write(f"Time: {datetime.datetime.now()}, Sentence: {sentence}\n")
    sentence_file.close()



