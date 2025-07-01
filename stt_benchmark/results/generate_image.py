# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 벤치마크 결과 CSV 파일 불러오기
benchmark_df = pd.read_csv("benchmark_results.csv")

# 모델명, 시간, 텍스트 분리
models = benchmark_df["Model"].tolist()
times = benchmark_df["Time (sec)"].tolist()

# 시각화
plt.figure(figsize=(10, 6))
bars = plt.bar(models, times, color='royalblue')

# 바 위에 숫자 표시
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

# 설정
plt.title('STT Benchmark Execution Time per Engine', fontsize=16)
plt.xlabel('Model', fontsize=12)
plt.ylabel('Execution Time (sec)', fontsize=12)
plt.ylim(0, max(times) * 1.2)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# 저장 및 출력
plt.savefig('stt_benchmark_chart.png')
plt.show()
