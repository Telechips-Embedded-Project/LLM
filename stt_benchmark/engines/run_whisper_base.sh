#!/bin/bash
START=$(date +%s.%N)
../whisper.cpp/build/bin/whisper-cli --output-txt harvard.wav.txt -f ../harvard.wav -m ../whisper.cpp/models/ggml-base.en.bin -t 8 
END=$(date +%s.%N)

ELAPSED=$(echo "$END - $START" | bc)
echo "Elapsed: $ELAPSED sec"

#cat jfk.wav.txt
