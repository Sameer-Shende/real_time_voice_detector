import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.signal import butter, lfilter

# Audio config
CHUNK = 1024
RATE = 16000
FORMAT = pyaudio.paInt16
CHANNELS = 1
THRESHOLD_DB = 45  # After bandpass filtering

# Buffers
energy_buffer = []
time_buffer = []

# Bandpass filter for 300–3000 Hz (typical voice band)
def butter_bandpass(lowcut, highcut, fs, order=4):
    from scipy.signal import butter
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    return butter(order, [low, high], btype='band')

def apply_bandpass_filter(data, lowcut=300, highcut=3000, fs=RATE):
    b, a = butter_bandpass(lowcut, highcut, fs)
    return lfilter(b, a, data)

# Computing band-limited energy
def compute_filtered_energy(data):
    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
    filtered = apply_bandpass_filter(audio_data)
    energy = np.sum(filtered**2) / len(filtered)
    return 10 * np.log10(energy + 1e-10)

def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("🎤 Listening (with bandpass)... Ctrl+C to stop.")
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            energy_db = compute_filtered_energy(data)
            energy_buffer.append(energy_db)
            time_buffer.append(time.time())

            if energy_db > THRESHOLD_DB:
                print(f"🔊 Voice-band energy detected at {time.strftime('%H:%M:%S')} ({energy_db:.2f} dB)")

    except KeyboardInterrupt:
        print("\n🛑 Stopped. Plotting...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    # Normalize time
    t0 = time_buffer[0]
    times = [t - t0 for t in time_buffer]

    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(times, energy_buffer, label="Filtered Energy (dB)")
    plt.axhline(y=THRESHOLD_DB, color='red', linestyle='--', label='Threshold')
    plt.xlabel("Time (s)")
    plt.ylabel("Energy in 300-3000 Hz Band (dB)")
    plt.title("Voice-Band Energy Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
