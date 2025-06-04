# Testing microphone using Vosk language model 
import os
import queue
import sys
import sounddevice as sd
import vosk
import json



# Path to the model
model_path = "C:\\Users\\Mariam\\Documents\\UAT\\UAT\\PDS400 - ProductionStudio400\\Assignment2\\Team-Alternative Drone Control\\.venv\\Lib\\site-packages\\vosk-model-small-en-us-0.15"

# Loading the model
if not os.path.exists(model_path):
    print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)

model = vosk.Model(model_path)

# Queue to hold audio data
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# To test microphone only
# Open an audio stream, code below 

# with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
#                     channels=1, callback=callback):
#    print('#' * 80)
#   print('Press Ctrl+C to stop the recording')
#    print('#' * 80)

#    rec = vosk.KaldiRecognizer(model, 16000)
#    while True:
#       data = q.get()
#       if rec.AcceptWaveform(data):
#           print(rec.Result())
#       else:
#           print(rec.PartialResult())

def process_command(command):
    if "go up" in command:
        print("Drone going up")
        # Drone code
    elif "go down" in command:
        print("Drone going down")
        # Drone code
    elif "stop listening" in command:
        print("Stopping listener")
        return True
    else:
        print("Unknown command")
    return False

def listen_and_process():
    # Opening audio stream
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                command = json.loads(result).get('text', '')
                if process_command(command):
                     return True  # Signal to stop the outer loop
    return False  # Continue the outer loop

# Continuous listening loop
print('#' * 40)
print('Listening for commands. Say "stop listener" to stop.')
print('#' * 40)

keep_listening = True
while keep_listening:
    keep_listening = not listen_and_process()

print("Listener completely stopped.")