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
        self.start_time = time.time()

    def update(self, *args):
        self.text = time.strftime('%I:%M %p')


Window.clearcolor = .3, .3, .3, 1


class WelcomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class ListeningScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


Builder.load_file("main.kv")


class mainApp(App):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    mainApp().run()
