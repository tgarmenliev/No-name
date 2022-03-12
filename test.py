# import speech_recognition
# import pyttsx3
# import os
# import sys
# import keyboard
# from datetime import datetime

# import recordingState

# def speechToText(self):
#     recogniser=speech_recognition.Recognizer()
#     resText = ""
#     while True:
#         try:
#             if recordingState.in_progress == False:
#                 break
#             with  speech_recognition.Microphone() as mic:
#                 recogniser.adjust_for_ambient_noise(mic)
#                 audio=recogniser.listen(mic)

#                 text=recogniser.recognize_google(audio)
#                 resText += text.lower()
#         except Exception:
#             continue

#     dir_path=sys.path[0]+"\\Recordings"
#     if os.path.isdir(dir_path)==False:
#         os.mkdir(dir_path)
#     # dir_path+=("\\"+str(datetime.today().strftime("%Y_%m_%d"))+"_"+str(datetime.now().strftime("%H_%M_%S")))
#     dir_path+=("\\"+self.textinput.text)
#     os.mkdir(dir_path)
#     name=dir_path+"\\TextFile.txt"
#     f=open(name,"w")
#     f.write(resText)
#     #there will be a summarizedFile.txt in dir_path 
#     f.close()

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
from pydub.utils import db_to_float
from pydub import AudioSegment 

def detect_silence(audio_segment, min_silence_len=1000, silence_thresh=-16, seek_step=1):
    """
    Returns a list of all silent sections [start, end] in milliseconds of audio_segment.
    Inverse of detect_nonsilent()

    audio_segment - the segment to find silence in
    min_silence_len - the minimum length for any silent section
    silence_thresh - the upper bound for how quiet is silent in dFBS
    seek_step - step size for interating over the segment in ms
    """
    seg_len = len(audio_segment)

    # you can't have a silent portion of a sound that is longer than the sound
    if seg_len < min_silence_len:
        return []

    # convert silence threshold to a float value (so we can compare it to rms)
    silence_thresh = db_to_float(silence_thresh) * audio_segment.max_possible_amplitude

    # find silence and add start and end indicies to the to_cut list
    silence_starts = []

    # check successive (1 sec by default) chunk of sound for silence
    # try a chunk at every "seek step" (or every chunk for a seek step == 1)
    last_slice_start = seg_len - min_silence_len
    slice_starts = range(0, last_slice_start + 1, seek_step)

    # guarantee last_slice_start is included in the range
    # to make sure the last portion of the audio is searched
    if last_slice_start % seek_step:
        slice_starts = itertools.chain(slice_starts, [last_slice_start])

    for i in slice_starts:
        audio_slice = audio_segment[i:i + min_silence_len]
        if audio_slice.rms <= silence_thresh:
            silence_starts.append(i)

    # short circuit when there is no silence
    if not silence_starts:
        return []

    # combine the silence we detected into ranges (start ms - end ms)
    silent_ranges = []

    prev_i = silence_starts.pop(0)
    current_range_start = prev_i

    for silence_start_i in silence_starts:
        continuous = (silence_start_i == prev_i + seek_step)

        # sometimes two small blips are enough for one particular slice to be
        # non-silent, despite the silence all running together. Just combine
        # the two overlapping silent ranges.
        silence_has_gap = silence_start_i > (prev_i + min_silence_len)

        if not continuous and silence_has_gap:
            silent_ranges.append([current_range_start,
                                  prev_i + min_silence_len])
            current_range_start = silence_start_i
        prev_i = silence_start_i

    silent_ranges.append([current_range_start,
                          prev_i + min_silence_len])

    return silent_ranges


def detect_nonsilent(audio_segment, min_silence_len=1000, silence_thresh=-16, seek_step=1):
    """
    Returns a list of all nonsilent sections [start, end] in milliseconds of audio_segment.
    Inverse of detect_silent()

    audio_segment - the segment to find silence in
    min_silence_len - the minimum length for any silent section
    silence_thresh - the upper bound for how quiet is silent in dFBS
    seek_step - step size for interating over the segment in ms
    """
    silent_ranges = detect_silence(audio_segment, min_silence_len, silence_thresh, seek_step)
    len_seg = len(audio_segment)

    # if there is no silence, the whole thing is nonsilent
    if not silent_ranges:
        return [[0, len_seg]]

    # short circuit when the whole audio segment is silent
    if silent_ranges[0][0] == 0 and silent_ranges[0][1] == len_seg:
        return []

    prev_end_i = 0
    nonsilent_ranges = []
    for start_i, end_i in silent_ranges:
        nonsilent_ranges.append([prev_end_i, start_i])
        prev_end_i = end_i

    if end_i != len_seg:
        nonsilent_ranges.append([prev_end_i, len_seg])

    if nonsilent_ranges[0] == [0, 0]:
        nonsilent_ranges.pop(0)

    return nonsilent_ranges


def split_on_silence(audio_segment, min_silence_len=1000, silence_thresh=-16, keep_silence=100,
                     seek_step=1):
    """
    Returns list of audio segments from splitting audio_segment on silent sections

    audio_segment - original pydub.AudioSegment() object

    min_silence_len - (in ms) minimum length of a silence to be used for
        a split. default: 1000ms

    silence_thresh - (in dBFS) anything quieter than this will be
        considered silence. default: -16dBFS

    keep_silence - (in ms or True/False) leave some silence at the beginning
        and end of the chunks. Keeps the sound from sounding like it
        is abruptly cut off.
        When the length of the silence is less than the keep_silence duration
        it is split evenly between the preceding and following non-silent
        segments.
        If True is specified, all the silence is kept, if False none is kept.
        default: 100ms

    seek_step - step size for interating over the segment in ms
    """

    # from the itertools documentation
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    if isinstance(keep_silence, bool):
        keep_silence = len(audio_segment) if keep_silence else 0

    output_ranges = [
        [ start - keep_silence, end + keep_silence ]
        for (start,end)
            in detect_nonsilent(audio_segment, min_silence_len, silence_thresh, seek_step)
    ]

    for range_i, range_ii in pairwise(output_ranges):
        last_end = range_i[1]
        next_start = range_ii[0]
        if next_start < last_end:
            range_i[1] = (last_end+next_start)//2
            range_ii[0] = range_i[1]

    return [
        audio_segment[ max(start,0) : min(end,len(audio_segment)) ]
        for start,end in output_ranges
    ]

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
        wav_file = AudioSegment.from_file(sys.path[0]+"\\test_recording.wav", format = "wav") 
        segments = split_on_silence(wav_file)
        for index in range(0, len(segments)):
            segments[index].export("segment_" + index + ".wav")
        print("loop stopped\n")
        for index in range(0, len(segments)):
            with  speech_recognition.AudioFile("segment_" + index + ".wav") as mic:
                audio=recogniser.record(mic)
                recogniser.adjust_for_ambient_noise(mic)
                #print(type(audio))
                text=recogniser.recognize_google(audio)
                text.lower()
                #print(text)
                resText.append(text + ". ")
        #mic.close()
        #os.remove(sys.path[0]+"\\test_recording.wav")

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
