import os
import datetime
import beepy

def play_beep(beep_name):
    '''
    Plays notification sounds with the sound that the user choose
    Args:
        beep_name: beep sound
    '''
    beepy.beep(sound=beep_name)


class Log:
    def __init__(self):
        self.full_date = datetime.datetime.now()

    def write_to_log(self, sentence):
        '''
        Respone to write to log the sentence in which one of the user's word was identified
        Args:
            sentence: the sentence that need to be written in the log

        '''
        filename = f"{self.full_date.strftime('%d%m%y')}_{self.full_date.strftime('%H%M%S')}_zoom_sentence.txt"

        if os.path.exists(filename):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not

        sentence_file = open(filename, append_write)
        sentence_file.write(f"Time: {datetime.datetime.now()}, Sentence: {sentence}\n")
        sentence_file.close()



