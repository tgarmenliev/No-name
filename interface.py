import kivy
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.widget import Widget

class PongApp(App):
    def build(self):
        return Label(text = "Hello World")

if __name__ == '__main__':
    PongApp().run()