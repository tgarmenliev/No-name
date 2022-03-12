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
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.core.window import Window

from functools import partial

import os
import sys
from threading import Thread

import recordingState
import STT
from STT import RecAUD

Window.clearcolor = '#0C0521'

kv="""
<RoundedButton@Button>:
    background_color: 0,0,0,0  # the last zero is the critical on, make invisible
    canvas.before:
        Color:
            rgba: (.882,.439,.322,1) if self.state=='normal' else (.055,.09,.02,1)  # visual feedback of press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]
<PlayButton@Button>:
    background_color: 0,0,0,0  # the last zero is the critical on, make invisible
    canvas.before:
        Color:
            rgba: (.882,.439,.322,1) if self.state=='normal' else (.055,.09,.02,1)  # visual feedback of press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15,]
            source: "images/play_icon.png"
<OriginalText@TextInput>
    size_hint: (1, .9)
    readonly: False
    background_color: 0, 0, 0, 0
    foreground_color: 1, 1, 1, 1
"""

class OriginalText(TextInput):
    pass

class PlayButton(Button):
    pass

class RoundedButton(Button):
    pass

Builder.load_string(kv)

class SpeechApp(App):

    # def on_enter(self, event):
    #     #self.textinput.text
    #     self.main_page(event)
    # def name_recording(self):
    #     self.window.clear_widgets()
    #     self.textinput = TextInput(multiline = False, size_hint = (1, .07), pos_hint = {'center_x':.5, 'center_y': .5})#padding_y = (20,20)
    #     self.textinput.bind(on_text_validate=self.on_enter)
    #     self.window.add_widget(Label(text = "Please name recording:", pos_hint = {'center_x':.5, 'center_y': .6}, font_size = "22sp"))
    #     self.window.add_widget(self.textinput)
    #     return self.window
        

    def stop_recording(self, instance):
        recordingState.in_progress = False
        #self.name_recording()
        self.main_page(instance)
    
    def stop_button(self, instance):
        recordingState.in_progress = True
        self.button = RoundedButton(text = 'Stop recording', on_press = self.stop_recording, font_size = "22sp",
                                    size_hint = (.5, .3), pos_hint = {'center_x':.5, 'center_y': .5}, bold = True)
        self.window.add_widget(self.button)
        return self.window
    
    def speech_to_text(self):
        Thread(target=RecAUD().speechToText, args=()).start()
        return self.window
    
    def start_recording(self, instance):
        self.window.clear_widgets()
        self.stop_button(instance)
        self.speech_to_text()
        return self.window
    
    def start_button(self, instance):
        self.window.clear_widgets()
        self.button1 = RoundedButton(text = 'Start recording', on_press = self.start_recording, font_size = "22sp",
                                    size_hint = (.7, .5), pos_hint = {'center_x':.5, 'center_y': .5}, bold = True)
        self.window.add_widget(self.button1)
        self.button2 = RoundedButton(text = 'Go back', on_press = self.main_page, font_size = "22sp",
                                    size_hint = (.2, .1), pos_hint = {'center_x':0, 'center_y': 1}, bold = True)
        self.window.add_widget(self.button2)
        return self.window

    def main_page(self, instance):
        self.window.clear_widgets()
        self.window.orientation = 'horizontal'
        self.button1 = RoundedButton(text = 'View recordings', on_press = self.view_recordings, font_size = "22sp",
                                    size_hint = (.55, .9), pos_hint = {'center_x':.15, 'center_y': .5}, bold = True)
        self.window.add_widget(self.button1)
        self.button2 = RoundedButton(text = 'Make new recording', on_press = self.start_button, font_size = "22sp",
                                    size_hint = (.55, .9), pos_hint = {'center_x': .85, 'center_y': .5}, bold = True)
        self.window.add_widget(self.button2)
        return self.window

    def build(self):
        self.window = FloatLayout()
        self.window.size_hint = (0.7, 0.8)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.button = RoundedButton(text = 'Get started', on_press = self.main_page, font_size = "22sp",
                                    size_hint = (.5, .3), pos_hint = {'center_x':.5, 'center_y': .5}, bold = True, padding = "10")
        self.window.add_widget(self.button)
        return self.window

    def view_recordings(self, instance):
        self.window.clear_widgets()
        #self.window.orientation = 'vertical'
        self.window.orientation = 'horizontal'
        old_path = os.getcwd()
        curr_path = os.getcwd() + "\Recordings"
        if os.path.isdir(curr_path)==False:
            os.mkdir(curr_path)
        os.chdir(curr_path)
        list_of_files = os.listdir()
        layout = GridLayout(size_hint_y = None, cols = 1,height = (Window.height/10 + 10)*len(list_of_files), width = Window.width) 
        layout.spacing = [5, 10]
        #layout.bind(minimum_height = self.window.setter('height'))
       # layout.orientation = 'vertical'
        self.button = RoundedButton(text = "Go back", on_press = self.main_page, font_size = "22sp",
                            size_hint = (.2, .1), pos_hint = {'center_x':0, 'center_y': 1}, bold = True)
        self.window.add_widget(self.button)
        self.buttons=[]
        
        list_of_files.reverse()
       # self.path=list_of_files
        for index in range(0,len(list_of_files)):
            self.buttons.append(RoundedButton(text = list_of_files[index], size_hint_y = None, height = Window.height / 10, font_size = "22sp",
                                            pos_hint = {'center_x':0, 'center_y': 1}, bold = True))
            self.buttons[index].bind(on_press = partial(self.recording,path=list_of_files[index]))
            layout.add_widget(self.buttons[index])  
        os.chdir(old_path) 
        root=ScrollView(size_hint=(1,1), size = (Window.size),do_scroll_x=False,do_scroll_y=True)
        root.add_widget(layout) 
        self.window.add_widget(root)
        return self.window
    
    def view_original_text(self,*args,**kwargs):
        #print(self.path[])
        path = kwargs.get("path")
        self.window.clear_widgets()
        self.window.orientation = 'vertical'
        self.button = RoundedButton(text = "Go back", on_press = partial(self.recording, path = path), font_size = "22sp",
                                    size_hint = (.2, .1), pos_hint = {'center_x':0, 'center_y': 1}, bold = True)
        #self.button.bind(on_press=partial(self.recording,path=path))
        self.window.add_widget(self.button)
        textfile = open("Recordings\\"+path+"\\TextFile.txt","r")
        text = textfile.read()
        self.label = OriginalText(text = text, font_size = "22sp", pos_hint = {'center_x': 0.5, 'center_y': 0.4}, font_name="Arial")
        self.window.add_widget(self.label)
        textfile.close()
        return self.window

    def view_summarized_text(self,*args,**kwargs):
        path = kwargs.get("path")
        self.window.clear_widgets()
        self.window.orientation = 'vertical'
        self.button = RoundedButton(text = "Go back", on_press = partial(self.recording, path = path), font_size = "22sp",
                                    size_hint = (.2, .1), pos_hint = {'center_x':0, 'center_y': 1}, bold = True)
        #self.button.bind(on_press=partial(self.recording,path=path))
        self.window.add_widget(self.button)
        textfile = open("Recordings\\"+path+"\\SummaryFile.txt","r")
        text = textfile.read()
        self.label = OriginalText(text = text, font_size = "22sp", pos_hint = {'center_x': 0.5, 'center_y': 0.4}, font_name="Arial")
        self.window.add_widget(self.label)
        textfile.close()
        return self.window

    def delete(self,instance,*args,**kwargs):
        self.window.clear_widgets()
        path = kwargs.get("path")
        os.remove("Recordings\\"+path+"\\TextFile.txt")
        os.remove("Recordings\\"+path+"\\SummaryFile.txt")
        os.rmdir("Recordings\\"+path)
        self.view_recordings(instance)
        return self.window

    def recording(self,*args,**kwargs):
        #print(instance)
        self.window.clear_widgets()
        self.window.orientation = 'vertical'
        #self.window.add_widget(Image(source = ''))
        self.button = RoundedButton(text = "Go back", on_press = self.view_recordings, font_size = "22sp",
                                    size_hint = (.2, .1), pos_hint = {'center_x':0, 'center_y': 1}, bold = True)
        self.window.add_widget(self.button) 
        self.button1 = RoundedButton(text = 'Original text', font_size = "22sp",
                                    size_hint = (.7, .3), pos_hint = {'center_x':.5, 'center_y': .85}, bold = True)
        path = kwargs.get("path")
        self.button1.bind(on_press = partial(self.view_original_text,path = path))
        #self.button1.bind(on_press=self.view_recordings)
        self.window.add_widget(self.button1)
        self.button2 = RoundedButton(text = 'Summary', font_size = "22sp",
                            size_hint = (.7, .3), pos_hint = {'center_x':.5, 'center_y': .5}, bold = True)
        self.button2.bind(on_press = partial(self.view_summarized_text,path = path))
        self.window.add_widget(self.button2)
        self.button3 = RoundedButton(text = 'Delete', font_size = "22sp",
                            size_hint = (.7, .3), pos_hint = {'center_x':.5, 'center_y': .15}, bold = True)
        self.button3.bind(on_press = partial(self.delete,path = path))
        self.window.add_widget(self.button3)
        #self.user = TextInput()
        return self.window

if __name__ == '__main__':
    SpeechApp().run()