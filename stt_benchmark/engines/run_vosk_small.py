# -*- coding: utf-8 -*-
import wave
import json
from vosk import Model, KaldiRecognizer

model = Model("../models/vosk-model-small-en-us-0.15")

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
    
    
with open("../results/vosk_small_result.txt", "w") as f:
    f.write(" ".join(results))

print("[RESULT]:", " ".join(results))
