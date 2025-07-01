# -*- coding: utf-8 -*-
import subprocess
import csv
import time
import os

# STT 모델 실행 정의
ENGINES = [
    ("vosk", ["python3", "engines/run_vosk.py"]),
    ("vosk-small", ["python3", "engines/run_vosk_small.py"]),
    ("whisper-base", ["bash", "engines/run_whisper_base.sh"]),
    ("whisper-tiny", ["bash", "engines/run_whisper_tiny.sh"])
]

results = []

for name, cmd in ENGINES:
    print(f"Running {name}...")

    # 정확한 시간 측정
    start = time.perf_counter()
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    end = time.perf_counter()
    elapsed = round(end - start, 2)

    output = result.stdout.decode(errors="ignore").strip()
    
    if name == "vosk" and os.path.exists("results/vosk_result.txt"):
        with open("results/vosk_result.txt", "r") as f:
          transcript = f.read().strip()
          
    elif name == "vosk-small" and os.path.exists("results/vosk_small_result.txt"):
        with open("results/vosk_small_result.txt", "r") as f:
          transcript = f.read().strip()

    # Whisper는 transcript를 jfk.wav.txt 파일에서 읽어옴
    if name.startswith("whisper") and os.path.exists("harvard.wav.txt"):
        with open("harvard.wav.txt", "r") as f:
            transcript = f.read().strip()


    results.append((name, elapsed, transcript))

# CSV 저장
os.makedirs("results", exist_ok=True)
with open("results/benchmark_results.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Model", "Time (sec)", "Transcript"])
    writer.writerows(results)

print("[TEST COMPLETE!] results/benchmark_results.csv SAVED.")
