#audio recorder with silence detection
import pyaudio
import wave
import numpy as np
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
SILENCE_THRESHOLD = 500  # RMS value
SILENCE_SECONDS = 30

class Recorder:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.recording = False

    def rms(self, data):
        shorts = np.frombuffer(data, dtype=np.int16)
        return np.sqrt(np.mean(shorts**2))

    def record(self, output="data/meeting.wav"):
        stream = self.p.open(format=FORMAT, channels=CHANNELS,
                             rate=RATE, input=True, frames_per_buffer=CHUNK)

        print("[*] Recording... Ctrl+C to stop.")
        self.frames = []
        self.recording = True
        silence_start = time.time()

        while self.recording:
            data = stream.read(CHUNK)
            self.frames.append(data)
            if self.rms(data) < SILENCE_THRESHOLD:
                if time.time() - silence_start > SILENCE_SECONDS:
                    break
            else:
                silence_start = time.time()

        stream.stop_stream()
        stream.close()
        self.p.terminate()

        with wave.open(output, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))
        print(f"[*] Saved: {output}")
        return output
