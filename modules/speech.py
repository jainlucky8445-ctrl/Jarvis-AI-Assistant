import edge_tts
import asyncio
import subprocess
import os
import time

ENGLISH_VOICE = "en-US-EricNeural"
HINDI_VOICE = "hi-IN-MadhurNeural"

current_process = None

def detect_hindi(text):
    hindi_chars = set('अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह')
    return any(char in hindi_chars for char in text)

async def speak_async(text):
    filename = f"jarvis_{int(time.time())}.mp3"
    if detect_hindi(text):
        voice = HINDI_VOICE
    else:
        voice = ENGLISH_VOICE
    communicate = edge_tts.Communicate(text, voice=voice, rate="+20%")
    await communicate.save(filename)
    return filename

def speak(text):
    global current_process
    try:
        print("Jarvis:", text)

        if current_process:
            current_process.terminate()
            current_process = None

        filename = asyncio.run(speak_async(text))

        current_process = subprocess.Popen(
            [r"D:\DOWNLOADS\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin\ffplay.exe",
             "-nodisp", "-autoexit", filename],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        current_process.wait()

        try:
            os.remove(filename)
        except:
            pass

    except Exception as e:
        print("Speech Error:", e)

def stop():
    global current_process
    if current_process:
        current_process.terminate()
        current_process = None