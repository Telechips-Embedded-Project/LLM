import pvporcupine
import pyaudio
import struct
import sounddevice as sd
import queue
import json
import time
import threading
from vosk import Model, KaldiRecognizer

AUDIO_RATE = 16000
q = queue.Queue()
recognize_now = False  # 공유 변수
model = Model("model")  # 모델은 1회만 로딩

# wake word detection 스레드
def wake_word_listener():
    global recognize_now
    porcupine = pvporcupine.create(
        access_key="IvEqb5BU5xECJZv+X3zRzYjbqMT/qQ92DiQ0REQk6l7obI1/XZfXGg==",
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

    print(">> Wake word 대기 중... ('Hi Telly')")
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        result = porcupine.process(pcm)
        if result >= 0:
            print(">> Wake word 감지됨!")
            recognize_now = True
            time.sleep(0.5)  # 감지 직후 약간의 텀

# vosk 스레드
def vosk_listener():
    global recognize_now
    recognizer = KaldiRecognizer(model, AUDIO_RATE)

    with sd.RawInputStream(samplerate=AUDIO_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=lambda indata, f, t, s: q.put(bytes(indata))):
        print(">> 마이크 시작됨.")
        while True:
            data = q.get()

            if not recognize_now:
                continue

            if recognizer.AcceptWaveform(data):
                res = json.loads(recognizer.Result())
                text = res.get("text", "")
                print("[인식 결과]:", text)

                # 상태 초기화
                recognize_now = False
                recognizer = KaldiRecognizer(model, AUDIO_RATE)  # 인식기 초기화
                print(">> 다시 wake word 대기 중...")

# 실행부
if __name__ == "__main__":
    thread1 = threading.Thread(target=wake_word_listener)
    thread2 = threading.Thread(target=vosk_listener)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
