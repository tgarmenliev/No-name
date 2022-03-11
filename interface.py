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
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout

import os
import sys
from threading import Thread

import recordingState
import STT
from STT import speechToText

class SpeechApp(App):
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
        self.window.orientation = 'horizontal'
        self.button1 = Button(text = 'View recordings')
        self.button1.bind(on_press=self.view_recordings)
        self.window.add_widget(self.button1)
        self.button2 = Button(text = 'Make new recording')
        self.button2.bind(on_press = self.start_recording)
        self.window.add_widget(self.button2)
        return self.window

    def build(self):
        self.window = BoxLayout()
        self.window.cols = 2
        self.button = Button(text = 'Get started')
        self.button.bind(on_press=self.main_page)
        self.window.add_widget(self.button)
        return self.window

    def view_recordings(self, instance):
        self.window.clear_widgets()
        self.window.orientation = 'vertical'
        self.button = Button(text = "Go back")
        self.button.bind(on_press=self.main_page)
        self.window.add_widget(self.button)      
        # self.window.add_widget(Label(text = "*List of recordings*"))
        old_path = os.getcwd()
        curr_path = os.getcwd() + "\Recordings"
        os.chdir(curr_path)
        list_of_files = os.listdir()
        for index in range(0, len(list_of_files)):
            self.button = Button(text = list_of_files[index])
            self.button.bind(on_press=self.recording)
            self.window.add_widget(self.button)  
        os.chdir(old_path)      
        return self.window
    
    def recording(self, instance):
        print(instance)
        self.window.clear_widgets()
        #self.window.add_widget(Image(source = ''))
        self.button = Button(text = "Go back")
        self.button.bind(on_press=self.view_recordings)
        self.window.add_widget(self.button) 
        self.button1 = Button(text = 'Original recording')
        #self.button1.bind(on_press=self.view_recordings)
        self.window.add_widget(self.button1)
        self.button2 = Button(text = 'Summary')
        self.window.add_widget(self.button2)
        #self.user = TextInput()
        return self.window

if __name__ == '__main__':
    SpeechApp().run()
