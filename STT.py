import speech_recognition
import pyttsx3

recogniser=speech_recognition.Recognizer()
button=False


while button==True:

    try:
        with  speech_recognition.Microphone() as mic:
            recogniser.adjust_for_ambient_noise(mic,duration=0.2)
            audio=recogniser.listen(mic)

            text=recogniser.recognize_google(audio)
            text=text.lower()

            print(f"Recognised {text}")

    except Exception:
        continue


