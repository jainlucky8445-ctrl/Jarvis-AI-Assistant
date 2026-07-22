import os
import sounddevice as sd
import soundfile as sf
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

ffmpeg_path = r"D:\DOWNLOADS\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin"
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Loading Faster Whisper...")
print("Faster Whisper Loaded!")

SAMPLERATE = 16000
DURATION = 4
MIC_DEVICE = 1

def take_command():
    try:
        print("\n🎤 Listening...")

        audio = sd.rec(
            int(DURATION * SAMPLERATE),
            samplerate=SAMPLERATE,
            channels=1,
            dtype="float32",
            device=MIC_DEVICE
        )

        sd.wait()

        sf.write("input.wav", audio, SAMPLERATE)

        print("🧠 Recognizing...")

        with open("input.wav", "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=("input.wav", f.read()),
                model="whisper-large-v3",
                response_format="text"
            )

        text = transcription.lower().strip()
        print("👤 You:", text)
        return text

    except Exception as e:
        print("Brain Error:", e)
        return ""