from gtts import gTTS
import os
file_path = "C:/Users/tisho/Desktop/Python_files/test.txt"
f = open(file_path, 'r')
str = f.read()
tts = gTTS(text=str, lang='en')
f.close()
tts.save("good.mp3")
os.system("start good.mp3")