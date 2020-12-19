
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from threading import Thread
import speechtotext
import time


class ClockText(Label):
    def __init__(self, **kwargs):
        super(ClockText, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
        self.start_time = time.time()

    def update(self, *args):
        self.text = time.strftime('%I:%M %p')


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
        # todo - check words list not empty
        self.manager.current = 'listening'
        self.listen_thread = Thread(target=speechtotext.speechToText, args=(words_list, sound_type, synonyms, write_to_log))
        self.listen_thread.start()


    def stop_listen(self):
        self.stop = True

    def infinite_loop(self, words_list, sound_type, synonyms, write_to_log):
        listen_thread = speechtotext.speechToText(words_list, sound_type, synonyms, write_to_log)
        listen_thread.start_speech_to_text()
        iteration = 0
        while True:
            if self.stop:
                # Stop running this thread so the main Python process can exit.
                return
            iteration += 1
            print('Infinite loop, iteration {}.'.format(iteration))


class ListeningScreen(Screen):
    def stop_listen(self):
        manager.current = 'settings'


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
