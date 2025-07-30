# app/audio_listener.py
import pyaudio
import wave
import threading
import numpy as np
import time

class AudioListener:
    def __init__(self, filename='meeting.wav', silence_threshold=500, silence_duration=30):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.frames = []
        self.filename = filename
        self.running = False
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.last_sound_time = time.time()

    def _is_silent(self, data):
        rms = np.sqrt(np.mean(np.square(np.frombuffer(data, dtype=np.int16))))
        return rms < self.silence_threshold

    def _record(self):
        pa = pyaudio.PyAudio()
        stream = pa.open(format=self.format,
                         channels=self.channels,
                         rate=self.rate,
                         input=True,
                         frames_per_buffer=self.chunk)
        print("Recording... (press Ctrl+C to stop)")
        while self.running:
            data = stream.read(self.chunk)
            self.frames.append(data)
            if not self._is_silent(data):
                self.last_sound_time = time.time()
            if time.time() - self.last_sound_time > self.silence_duration:
                print("Silence detected. Stopping...")
                self.running = False
                break
        stream.stop_stream()
        stream.close()
        pa.terminate()

    def start(self):
        self.frames = []
        self.running = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def save_buffer(self):
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        return self.filename
