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

import time


class ClockText(Label):
    def __init__(self, **kwargs):
        super(ClockText, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = '\n\n' + time.strftime('%H:%M:%S')


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
        self.start_time = time.time()
        self.manager.current = 'listening'


class ListeningScreen(Screen):
    def stop_listen(self):
        self.manager.current = 'settings'


class ScreenManagement(ScreenManager):
    pass


Builder.load_file("main.kv")


class mainApp(App):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    mainApp().run()
