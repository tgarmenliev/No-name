from gtts import gTTS
import os
message = input()
tts = gTTS(text=message, lang='en')
tts.save("good.mp3")
os.system("start good.mp3")