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


class MyThread(Thread):
    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

        # function using _stop function

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while True:
            if self.stopped():
                return
            print("Hello, world!")
            time.sleep(1)


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
    if len(wordslist) == 0:
        show_warning_popup("Words list can't be empty")
        return False
    for word in wordslist:
        if not word.isalpha():
            show_warning_popup("Words must contain only alphabets")
            return False
    return True


class ClockText(Label):
    def __init__(self, **kwargs):
        super(ClockText, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
        self.start_time = time.time()

    def update(self, *args):
        self.text = '\n' + time.strftime('%I:%M %p')


Window.clearcolor = .3, .3, .3, 1


class WelcomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    def fetch_input(self):
        # words input
        words_list = self.ids.words.text.split(",")
        words_list = list(map(str.strip, words_list))
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
        # Get the inputs from the GUI
        words_list, sound_type, synonyms, write_to_log = self.fetch_input()
        if not check_words_list(words_list):
            return
        # todo - check words list not empty
        self.manager.current = 'listening'
        self.manager.children[0].ids.words_search.text = ", ".join(words_list)
        self.manager.listen_thread = speechtotext.speechToText(words_list, sound_type, synonyms, write_to_log)
        self.manager.listen_thread.daemon = True
        self.manager.listen_thread.start()


    # def stop_listen(self):
    #     self.stop = True

    # def infinite_loop(self, words_list, sound_type, synonyms, write_to_log):
    #     listen_thread = speechtotext.speechToText(words_list, sound_type, synonyms, write_to_log)
    #     listen_thread.start_speech_to_text()
    #     iteration = 0
    #     while True:
    #         if self.stop:
    #             # Stop running this thread so the main Python process can exit.
    #             return
    #         iteration += 1
    #         print('Infinite loop, iteration {}.'.format(iteration))


class ListeningScreen(Screen):
    def stop_listen(self):
        self.manager.listen_thread.stop()
        self.manager.current = 'settings'


class ScreenManagement(ScreenManager):
    pass


Builder.load_file("main.kv")


class mainApp(App):
    def build(self):
        screen_management = ScreenManagement()
        return screen_management


if __name__ == '__main__':
    # gui_thread = Thread(target=ScreenManagement, daemon=True)
    # gui_thread.start()
    # # listen_thread.start()
    mainApp().run()
