# Incorporating Speech Recognition to Drone Commands

# import pygame 
# speech recognition library to work with speech recognition engines
import speech_recognition as sr 
import pyaudio
# pocketsphinx is installed - pip install pocketsphinx

recognizer = sr.Recognizer()


# Function to recognize speech from the microphone
def recognize_speech_from_mic():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for speech...")

        # Capture the audio data
        audio_data = recognizer.listen(source)

        try:
            # Recognize speech using Sphinx
            text = recognizer.recognize_sphinx(audio_data)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Sphinx could not understand the audio")
        except sr.RequestError as e:
            print(f"Sphinx error; {e}")

# Call the function to recognize speech from the microphone
recognize_speech_from_mic()