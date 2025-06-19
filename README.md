# 🗣️ Real-Time Voice Activity Detection (VAD) in Python

This project implements a real-time voice activity detector in Python using `PyAudio`, `NumPy`, and `Matplotlib`. It captures audio from the microphone, filters it to the human speech frequency band (300–3000 Hz), computes the energy in dB, and detects voice segments. After stopping the recording, it plots the energy levels over time.

---

## 🔧 Features

- 🎤 Real-time microphone input
- 🎚️ Bandpass filter to isolate human voice (300–3000 Hz)
- 📈 Log-scaled energy (dB) computation
- 🧠 Voice activity printed to terminal when threshold is exceeded
- 📊 Final plot of energy over time (after you stop recording)

---

## 🛠️ Requirements and how to run the code

Install the following Python libraries:

```bash
pip install pyaudio numpy matplotlib scipy
python main.py
