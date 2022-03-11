import speech_recognition
import pyttsx3
import os
import sys
import keyboard

recogniser=speech_recognition.Recognizer()
button=False
text=""
while True:
    if keyboard.read_key()=="a":
        button = True
        break

while button==True:

    try:
        if keyboard.read_key()=="s":
            button = False
            break
        if button == True:
            with  speech_recognition.Microphone() as mic:
                recogniser.adjust_for_ambient_noise(mic)
                audio=recogniser.listen(mic)

                text=recogniser.recognize_google(audio)
                text=text.lower()

                

    except Exception:
        continue

#print(f"Recognised {text}")
index_file=open(os.path.join(sys.path[0],"STT_Index_File.txt"),"r")
try:
    index=int(index_file.read())
    index_file=open(os.path.join(sys.path[0],"STT_Index_File.txt"),"w")
    index_file.write(str(index+1))
    index_file.close()

    name="STT_Original_"+str(index)+".txt"
    f=open(name,"w")
    f.write(text)
    f.close()
except ValueError:
    pass
