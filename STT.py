import speech_recognition
import pyttsx3
import os
import sys

recogniser=speech_recognition.Recognizer()
button=False


while button==True:

    try:
        if button == True:
            with  speech_recognition.Microphone() as mic:
                recogniser.adjust_for_ambient_noise(mic)
                audio=recogniser.listen(mic)

                text=recogniser.recognize_google(audio)
                text=text.lower()

                #print(f"Recognised {text}")

    except Exception:
        continue

index_file=open(os.path.join(sys.path[0],"STT_Index_File.txt"),"r")
try:
    index=int(index_file.read())
    index_file=open(os.path.join(sys.path[0],"STT_Index_File.txt"),"w")
    index_file.write(str(index+1))
    index_file.close()

    name="STT_Original_"+str(index)
    f=open(name,"w")
    f.write(text)
    f.close()
except ValueError:
    pass
