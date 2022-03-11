import speech_recognition
import pyttsx3
import os
import sys
import keyboard
from datetime import datetime
def SpeechToText():
    recogniser=speech_recognition.Recognizer()
    text=""
    while True:
        try:
            if recording.in_progress==False:
                break
            with  speech_recognition.Microphone() as mic:
                recogniser.adjust_for_ambient_noise(mic)
                audio=recogniser.listen(mic)

                text=recogniser.recognize_google(audio)
                text=text.lower()

                    

        except Exception:
            continue

#print(f"Recognised {text}")
#index_file=open(os.path.join(sys.path[0],"STT_Index_File.txt"),"r")
#try:
#    index=int(index_file.read())
#    index_file=open(os.path.join(sys.path[0],"STT_Index_File.txt"),"w")
#    index_file.write(str(index+1))
#    index_file.close()

    name=sys.path[0]+"\\Recordings\\TextFile_" + str(datetime.today().strftime("%Y_%M_%D"))+"_"+str(datetime.now().strftime("%H_%M_%S"))+".txt"
    f=open(name,"w")
    f.write(text)
    f.close()
