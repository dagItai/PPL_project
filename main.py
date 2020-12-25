import threading
import time
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

import speechtotext

Window.clearcolor = .3, .3, .3, 1

def show_warning_popup(text):
    '''
    Responsible for create and preform the pop window for error message
    :param text: which text should appear on the popup
    '''
    layout = GridLayout(cols=1, rows=2, padding=5)
    popupLabel = Label(text=text, padding=(50, 50), halign="center", valign="middle", size_hint=(1.0, 1.0),
                       color=(0.51764, 0.74117, 0.99607, 1), font_name='Sofia-Pro-Light-Az')
    closeButton = Button(text="Close me!", background_normal='button.JPG',
                         color=(0.51764, 0.74117, 0.99607, 1), font_name='Sofia-Pro-Light-Az')
    layout.add_widget(popupLabel)
    layout.add_widget(closeButton)
    # Instantiate the modal popup and display
    popup = Popup(title='Warning',
                  content=layout, size_hint=(None, None), size=(280, 170), background='popup.JPG', title_color=(0.51764, 0.74117, 0.99607, 1), title_font='Sofia-Pro-Light-Az')
    popup.open()
    # Attach close button press with popup.dismiss action
    closeButton.bind(on_press=popup.dismiss)

def check_words_list(wordslist):
    '''
    Check that the wordslist is not empty and that all the words entered consist only alphabet letters
    Args:
        wordslist: List of words taken from the GUI when separated by a comma
    Returns: True if the list not empty and all the words are alphabet, False otherwise and raise an warning pop up
    '''
    if len(wordslist) == 0:
        show_warning_popup("Words list can't be empty")
        return False
    for word in wordslist:
        if not all(x.isalpha() or x.isspace() for x in word):
            show_warning_popup("Words must contain only alphabets\nMake sure you separate the\nwords by comma")
            return False
    return True

class WelcomeScreen(Screen):
    '''
    First svreen in app
    '''
    pass

class SettingsScreen(Screen):
    '''
    The second window in the app, where the user set all the parameters
    '''
    def fetch_input(self):
        '''
        Responsible for get the parameter that the user have been set in the GU
        Returns:
            4 parameter that the user set: words_list, sound_type, synonyms, write_to_log
        '''
        # words input
        if self.ids.words.text:
            words_list = self.ids.words.text.split(",")
            words_list = [i.strip() for i in words_list]
        else:
            words_list = list()
        # sound type
        sound_type = self.ids.dropdownmain.text.split(":")
        if len(sound_type) > 1:
            sound_type = sound_type[1].strip()
        else:
            sound_type = 'success'
        # synonyms
        synonyms = self.ids.synonyms.active
        # write to log
        write_to_log = self.ids.log.active
        return words_list, sound_type, synonyms, write_to_log

    # Responsible for the listen
    def start_listen(self):
        '''
        The main function which run the all process after clicking on the "start listen" button
        '''
        # Get the inputs from the GUI
        words_list, sound_type, synonyms, write_to_log = self.fetch_input()
        # Check that the input is valid
        if not check_words_list(words_list):
            return
        self.manager.current = 'listening'
        self.manager.children[0].ids.words_search.text = ", ".join(words_list)
        # Start the listen thread that do speech-to-text
        self.manager.listen_thread = speechtotext.speechToText(words_list, sound_type, synonyms, write_to_log)
        self.manager.listen_thread.daemon = True
        self.manager.listen_thread.start()

class ListeningScreen(Screen):
    '''
    The third screen in the app, when the speech to text process takes place
    '''
    def stop_listen(self):
        '''
        Stopping the listen_thread after the user clicking "stop listen"
        '''
        self.manager.listen_thread.stop()
        self.manager.current = 'settings'

class ClockText(Label):
    '''
    Clock that appears in the third window
    '''
    def __init__(self, **kwargs):
        super(ClockText, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
        self.start_time = time.time()

    def update(self, *args):
        self.text = '\n' + time.strftime('%I:%M %p')

class ScreenManagement(ScreenManager):
    pass

class mainApp(App):
    def build(self):
        screen_management = ScreenManagement()
        return screen_management

Builder.load_file("main.kv")


if __name__ == '__main__':
    mainApp().run()
