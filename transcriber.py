#whisper Transcription
import whisper

model = whisper.load_model("tiny")

def transcribe(audio_path):
    print("[*] Transcribing...")
    result = model.transcribe(audio_path)
    return result["text"]
