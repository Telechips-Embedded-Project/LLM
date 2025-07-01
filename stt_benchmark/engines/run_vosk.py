# -*- coding: utf-8 -*-
'''
import pvporcupine
import pyaudio
import struct
import sounddevice as sd
import queue
import json
import time
import threading
from vosk import Model, KaldiRecognizer
import sys
import io


AUDIO_RATE = 16000
q = queue.Queue()
recognize_now = False 
model = Model("../models/vosk-model-en-us-0.22")  


def wake_word_listener():
    global recognize_now
    porcupine = pvporcupine.create(
        access_key="qvg3+n8HIzQe1zCVVhps8yXTNYjlGO52eQ7RTk9T5/E90OS7+KespA==",
        keyword_paths=["porcupine/bumblebee_raspberry-pi.ppn"]
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print(">> Wake word waiting... ('Hi Telly')")
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        result = porcupine.process(pcm)
        if result >= 0:
            print(">> Wake word Detected!")
            recognize_now = True
            time.sleep(0.5) 
            
            

def vosk_listener():
    global recognize_now
    recognizer = KaldiRecognizer(model, AUDIO_RATE)

    with sd.RawInputStream(samplerate=AUDIO_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=lambda indata, f, t, s: q.put(bytes(indata))):
        print(">> Listening...")
        while True:
            data = q.get()

            if not recognize_now:
                continue

            if recognizer.AcceptWaveform(data):
                res = json.loads(recognizer.Result())
                text = res.get("text", "")
                print("[RESULT]:", text)

                
                recognize_now = False
                recognizer = KaldiRecognizer(model, AUDIO_RATE)  
                print(">> Wake word waiting...")


if __name__ == "__main__":
    thread1 = threading.Thread(target=wake_word_listener)
    thread2 = threading.Thread(target=vosk_listener)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
'''





# -*- coding: utf-8 -*-
import wave
import json
from vosk import Model, KaldiRecognizer

model = Model("../models/vosk-model-en-us-0.22")

wf = wave.open("../harvard.wav", "rb")
rec = KaldiRecognizer(model, wf.getframerate())

results = []
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        if res.get("text"):
            results.append(res["text"])

final = json.loads(rec.FinalResult())
if final.get("text"):
    results.append(final["text"])

with open("../results/vosk_result.txt", "w") as f:
    f.write(" ".join(results))

print("[RESULT]:", " ".join(results))

