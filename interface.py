import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.clock import Clock

from threading import Thread

import recordingState
import STT
from STT import speechToText

class Interface(App):

    def stop_recording(self, instance):
        recordingState.in_progress = False
        self.main_page(instance)
    
    def stop_button(self, instance):
        recordingState.in_progress = True
        self.button = Button(text = 'Stop recording')
        self.button.bind(on_press = self.stop_recording)
        self.window.add_widget(self.button)
        return self.window
    
    def speech_to_text(self):
        Thread(target=STT.speechToText, args=()).start()
        return self.window
    
    def start_recording(self, instance):
        self.window.clear_widgets()
        self.stop_button(instance)
        self.speech_to_text()
        return self.window
    
    def main_page(self, instance):
        self.window.clear_widgets()
        self.button = Button(text = 'View recordings')
        self.button.bind(on_press=self.view_recordings)
        self.window.add_widget(self.button)
        self.button = Button(text = 'Make new recording')
        self.button.bind(on_press = self.start_recording)
        self.window.add_widget(self.button)
        return self.window

    def build(self):
        self.window = BoxLayout()
        self.window.cols = 1
        self.button = Button(text = 'Get started')
        self.button.bind(on_press=self.main_page)
        self.window.add_widget(self.button)
        return self.window

    def view_recordings(self, instance):
        self.window.clear_widgets()
        self.window = BoxLayout()
        self.button = Button(text = "Go back")
        self.button.bind(on_press=self.main_page)
        self.window.add_widget(self.button)
        self.window.add_widget(Label(text = "List of recordings"))
        return self.window

if __name__ == '__main__':
    Interface().run()
