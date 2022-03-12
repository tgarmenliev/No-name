# import speech_recognition
# import pyttsx3
# import os
# import sys
# import keyboard
# import wave
# from datetime import datetime
# from threading import Thread
# import recordingState
# import pyaudio

# import itertools
# from pydub import AudioSegment
# from pydub.silence import split_on_silence

# import text_summary
# from text_summary import generate_summary

# def split(file):
#     sound = AudioSegment.from_wav(file)
#     # spliting audio files
#     audio_chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=-50 )
#     #loop is used to iterate over the output list
#     for i, chunk in enumerate(audio_chunks):
#         output_file = sys.path[0]+"\\segment_recording_{0}.wav".format(i)
#         print("Exporting file", output_file)
#         chunk.export(output_file, format="wav")
#     return len(audio_chunks)
# #import text_summary
# #from text_summary import generate_summary
# class RecAUD:
#     def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=1, rate=44100, py=pyaudio.PyAudio()):
#         self.collections = []
#         self.CHUNK = chunk
#         self.FORMAT = frmat
#         self.CHANNELS = channels
#         self.RATE = rate
#         self.p = py
#         self.st = 1
#         self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

#     def start_record(self):
#         self.st = 1
#         self.frames = []
#         stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
#         while self.st == 1:
#             data = stream.read(self.CHUNK)
#             self.frames.append(data)
#            # print("* recording")
#             #self.main.update()
#         print("actually loop stopped")
#         stream.close()

#         wf = wave.open('test_recording.wav', 'wb')
#         print("create wave")
#         wf.setnchannels(self.CHANNELS)
#         wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
#         wf.setframerate(self.RATE)
#         wf.writeframes(b''.join(self.frames))
#         wf.close()
#         print ("audio file ready\n")

#     def stop(self):
#         self.st = 0

#     def speechToText(self):
#         recogniser=speech_recognition.Recognizer()
#         resText = ""
        
#         print("start\n")
#         #self.start_record()
#         th=Thread(target=self.start_record,args=())
#         th.start()
#         while recordingState.in_progress == True:
#         #while  keyboard.read_key()!="a":
#             pass
#         self.stop()
#         th.join()
#         #wav_file = AudioSegment.from_file(sys.path[0]+"\\test_recording.wav", format = "wav") 
#         l=split(sys.path[0]+"\\test_recording.wav")
#         #for index in range(0, len(segments)):
#          #   segments[index].export("segment_" + index + ".wav")
#         print("loop stopped\n")
#         for index in range(0, l):
#             with  speech_recognition.AudioFile("segment_recording_" + str(index) + ".wav") as mic:
#                 audio=recogniser.record(mic)
#                 recogniser.adjust_for_ambient_noise(mic)
#                 #print(type(audio))
#                 try:
#                     text=recogniser.recognize_google(audio)
#                 except:
#                     text=""
#                 text.lower()
#                 #print(text)
#                 resText+=(text + ". ")
                
#                 #os.remove("segment_recording_" + str(index) + ".wav")
#         #os.remove(sys.path[0]+"\\test_recording.wav")
#         os.remove("test_recording.wav")
#         for index in range(0, l):
#             os.remove("segment_recording_" + str(index) + ".wav")
#         dir_path=sys.path[0]+"\\Recordings"
#         if os.path.isdir(dir_path)==False:
#             os.mkdir(dir_path)
#         name = ''
#         while recordingState.textinput == '':
#             name = ("\\" + recordingState.textinput)
#         dir_path += ("\\" + recordingState.textinput)
#         os.mkdir(dir_path)
#         name=dir_path+"\\TextFile.txt"
#         f=open(name,"w")
#         f.write(resText)
#         f.close()
#         generate_summary(name,l//3+1)

# #RecAUD().speechToText()

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

import itertools
from pydub import AudioSegment
from pydub.silence import split_on_silence

import text_summary
from text_summary import generate_summary

def split(file):
    sound = AudioSegment.from_wav(file)
    # spliting audio files
    audio_chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=-40)
    #loop is used to iterate over the output list
    for i, chunk in enumerate(audio_chunks):
        output_file = sys.path[0]+"\\segment_recording_{0}.wav".format(i)
        print("Exporting file", output_file)
        chunk.export(output_file, format="wav")
    return len(audio_chunks)
#import text_summary
#from text_summary import generate_summary
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
        print("actually loop stopped")
        stream.close()

        wf = wave.open('test_recording.wav', 'wb')
        print("create wave")
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
        th=Thread(target=self.start_record,args=())
        th.start()
        while recordingState.in_progress == True:
        #while  keyboard.read_key()!="a":
            pass
        self.stop()
        th.join()
        #wav_file = AudioSegment.from_file(sys.path[0]+"\\test_recording.wav", format = "wav") 
        l=split(sys.path[0]+"\\test_recording.wav")
        #for index in range(0, len(segments)):
         #   segments[index].export("segment_" + index + ".wav")
        print("loop stopped\n")
        for index in range(0, l):
            with  speech_recognition.AudioFile("segment_recording_" + str(index) + ".wav") as mic:
                audio=recogniser.record(mic)
                recogniser.adjust_for_ambient_noise(mic)
                #print(type(audio))
                try:
                    text=recogniser.recognize_google(audio)
                except:
                    text=""
                text.lower()
                #print(text)
                resText+=(text + ". ")
                
                #os.remove("segment_recording_" + str(index) + ".wav")
        #os.remove(sys.path[0]+"\\test_recording.wav")
        for index in range(0, l):
           os.remove(sys.path[0] + "\\segment_recording_" + str(index) + ".wav")
        os.remove(sys.path[0]+"\\test_recording.wav")
        dir_path=sys.path[0]+"\\Recordings"
        if os.path.isdir(dir_path)==False:
            os.mkdir(dir_path)
        name = ''
        while recordingState.textinput == '':
            name = ("\\" + recordingState.textinput)
        dir_path += ("\\" + recordingState.textinput)
        os.mkdir(dir_path)
        name=dir_path+"\\TextFile.txt"
        f=open(name,"w")
        f.write(resText)
        f.close()
        generate_summary(name,l//3+1)

#RecAUD().speechToText()
