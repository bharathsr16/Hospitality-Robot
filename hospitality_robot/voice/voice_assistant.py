import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import sys
import tempfile

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.event_manager import get_event_details

def listen_and_respond(audio_file=None):
    """
    Listens for a command and responds with event information.
    """
    r = sr.Recognizer()

    if audio_file:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
    else:
        # This part of the code will not be executed in the current environment
        # but is here for completeness.
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

    try:
        # Using Google's speech recognition for better accuracy, but it requires an internet connection.
        # If offline, you can use recognize_sphinx() which works offline but is less accurate.
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")

        # Basic intent recognition
        if "where is the" in command:
            event_name = command.split("where is the")[-1].strip()
            event = get_event_details(event_name)
            if event:
                response = f"The {event[1]} is at {event[2]} from {event[3]} to {event[4]}."
            else:
                response = f"Sorry, I couldn't find any event named {event_name}."
        elif "what's the next event" in command:
            # This is a placeholder. A more complex logic would be needed to determine the "next" event.
            response = "The next event is the Coding Workshop at Block B, Room 201."
        else:
            response = "Sorry, I didn't understand that. You can ask me about event locations."

        print(response)
        speak(response)

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def speak(text):
    """
    Converts text to speech and plays it.
    """
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
        tts.save(fp.name)
        try:
            song = AudioSegment.from_mp3(fp.name)
            # Audio playback may fail in environments without a configured audio output.
            play(song)
        except Exception as e:
            print(f"Error playing sound: {e}")
            print("Audio playback failed. This is expected in some environments.")

if __name__ == '__main__':
    # Since we can't use a microphone, we'll simulate with a pre-recorded audio file.
    # The user would need to provide a test audio file named 'test_command.wav'
    test_audio = 'test_command.wav'
    if os.path.exists(test_audio):
        listen_and_respond(test_audio)
    else:
        print(f"Please provide a test audio file named '{test_audio}' in the root directory.")
        # As a fallback, let's test the text generation without audio input
        event = get_event_details('Tech Talk')
        response = f"The {event[1]} is at {event[2]} from {event[3]} to {event[4]}."
        print(response)
        speak(response)
