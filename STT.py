import speech_recognition
import pyttsx3
import os
import sys
import keyboard
import wave
from datetime import datetime
from threading import Thread
import recordingState
import pyaudio

import text_summary
from text_summary import generate_summary
class RecAUD:
    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=1, rate=44100, py=pyaudio.PyAudio()):
        self.collections = []
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

    def start_record(self):
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
           # print("* recording")
            #self.main.update()

        stream.close()

        wf = wave.open('test_recording.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print ("audio file ready\n")

    def stop(self):
        self.st = 0

    def speechToText(self):
        recogniser=speech_recognition.Recognizer()
        resText = ""
        
        print("start\n")
        #self.start_record()
        Thread(target=self.start_record,args=()).start()
        while recordingState.in_progress == True:
        #while  keyboard.read_key()!="a":
            pass
        self.stop()
        print("loop stopped\n")
        with  speech_recognition.AudioFile(sys.path[0]+"\\test_recording.wav") as mic:

            audio=recogniser.record(mic)
            recogniser.adjust_for_ambient_noise(mic)
            #print(type(audio))
            resText=recogniser.recognize_google(audio)
            resText.lower()
            print(resText)

        dir_path=sys.path[0]+"\\Recordings"
        if os.path.isdir(dir_path)==False:
            os.mkdir(dir_path)
        dir_path+=("\\"+str(datetime.today().strftime("%Y_%m_%d"))+"_"+str(datetime.now().strftime("%H_%M_%S")))
        os.mkdir(dir_path)
        name=dir_path+"\\TextFile.txt"
        f=open(name,"w")
        f.write(resText)
        f.close()
       # generate_summary(name,1)

#RecAUD().speechToText()
