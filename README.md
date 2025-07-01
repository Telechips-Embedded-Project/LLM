<aside>

### Vosk, Vosk_small, Whisper.cpp_base, Whisper.cpp_tiny 
4 모델 성능 분석 및 지표(matplotlib) 자동 생성 프로그램 개발 [완료]

STT 결과(.wav → .txt) 확인(정확도) 및 실행되는데 걸리는 시간(실행 시작부터 종료까지) 측정. <br>
객관적인 지표를 위해 동일 환경을 구축하고, 하나의 시스템으로 개발. <br>

</aside>

**전체 디렉토리 구조 (benchmark 시스템)**

```bash
stt_benchmark/
├── jfk.wav, harvard.wav, sample1.wav
│          
├── models/
│   ├── vosk-model-en-us-0.22
│   ├── vosk-model-small-en-us-0.15
│   ├── ggml-base.en.bin
│   └── ggml-tiny.en.bin
├── benchmark.py       # 전체 벤치마크 실행 스크립트
├── engines/
│   ├── run_vosk.py
│   ├── run_vosk_small.py
│   ├── run_whisper_base.sh
│   └── run_whisper_tiny.sh
└── results/
    └── benchmark_results.csv  # 자동 측정 결과 저장
    └── generate_image.py  # 성능지표 (pandas,matplotlib)
```

**실행 방법**

```bash
source ~/.venv/bin/activate  #가상환경 진입
cd stt_benchmark

python3 benchmark.py
```

**실행 결과 (.csv, .png)**

[benchmark_results.csv](attachment:9d554c34-8ae6-4f8d-891d-cff5d4a78bc7:benchmark_results.csv)

```
Model,Time (sec),Transcript
vosk,0.52,and so my fellow americans ask not what your country can do for you ask what you can do for your country
vosk-small,0.52,and so my fellow americans as not what your country can do for you ask what you can do for your country
whisper-base,0.43,"And so my fellow Americans, ask not what your country can do for you, ask what you can do for your country."
whisper-tiny,0.02,"And so my fellow Americans, ask not what your country can do for you, ask what you can do for your country."
```

![STT_result.png](https://github.com/user-attachments/assets/e1b1ed97-255e-4ee0-a125-ded833472c4d)

<aside>

**실험 결과**

whisper-tiny가 압도적으로 빠르고 정확도도 크게 떨어지지 않음. (총 sample 3개로 비교하였음)

따라서 whisper-tiny로 LLM 시스템의 STT 부분 구현하기로 결정.

whisper.cpp 특성 상 실시간 스트리밍은 불가하나, tiny 모델의 빠른 속도로 인하여 파일 입출력 방식(음성 녹음 → .wav → .txt)을 이용한 준실시간 STT 구현이 가능할 것으로 기대됨.

</aside>
