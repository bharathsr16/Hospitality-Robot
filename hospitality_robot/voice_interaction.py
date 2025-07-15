import speech_recognition as sr
import pyttsx3

def listen():
    """
    Listens for voice input from the user.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def speak(text):
    """
    Speaks the given text.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
