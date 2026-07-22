from modules.apps import open_app, close_app
from modules.ai import ask_ai
from modules.speech import speak, stop
from modules.brain import take_command
from modules.memory import load_memory, add_note, get_notes
from modules.entertainment import (
    get_cricket_score, get_football_score,
    get_movie_recommendation, get_quote,
    flip_coin, roll_dice
)
import datetime
import webbrowser
import numpy as np
import sounddevice as sd
from openwakeword.model import Model
import psutil
import requests
import screen_brightness_control as sbc
import subprocess
import os
import time
import wikipedia
from dotenv import load_dotenv

load_dotenv()

# Wake word model load karo
print("Loading Wake Word Model...")
oww_model = Model(wakeword_models=["hey jarvis"], inference_framework="onnx")
print("Wake Word Model Loaded!")

SAMPLERATE = 16000
CHUNK = 512
MIC_DEVICE = 1
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Agra"

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"The weather in {CITY} is {desc} with temperature {temp} degrees celsius"
    except:
        return "Sorry, I could not fetch the weather right now"

def take_screenshot():
    try:
        from PIL import ImageGrab
        filename = f"screenshot_{int(time.time())}.png"
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        return "Screenshot saved successfully"
    except:
        return "Sorry, could not take screenshot"

def get_battery():
    try:
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = "charging" if battery.power_plugged else "not charging"
        return f"Battery is at {int(percent)} percent and {plugged}"
    except:
        return "Could not get battery status"

def get_system_status():
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        return f"CPU usage is {cpu} percent and RAM usage is {ram} percent"
    except:
        return "Could not get system status"

def set_volume(action):
    try:
        if action == "up":
            for i in range(5):
                subprocess.run(
                    'powershell -c "(New-Object -comObject WScript.Shell).SendKeys([char]175)"',
                    shell=True
                )
        elif action == "down":
            for i in range(5):
                subprocess.run(
                    'powershell -c "(New-Object -comObject WScript.Shell).SendKeys([char]174)"',
                    shell=True
                )
        elif action == "mute":
            subprocess.run(
                'powershell -c "(New-Object -comObject WScript.Shell).SendKeys([char]173)"',
                shell=True
            )
        return True
    except:
        return False

def set_brightness(level):
    try:
        sbc.set_brightness(level)
        return True
    except:
        return False

def summarize_website(url):
    try:
        response = requests.get(url, timeout=5)
        from html.parser import HTMLParser

        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.skip = False

            def handle_starttag(self, tag, attrs):
                if tag in ["script", "style", "nav", "footer"]:
                    self.skip = True

            def handle_endtag(self, tag):
                if tag in ["script", "style", "nav", "footer"]:
                    self.skip = False

            def handle_data(self, data):
                if not self.skip and data.strip():
                    self.text.append(data.strip())

        parser = TextExtractor()
        parser.feed(response.text)
        text = " ".join(parser.text[:100])
        summary = ask_ai(f"Summarize this in 2-3 sentences: {text[:1000]}")
        return summary
    except:
        return "Sorry, I could not summarize that website"

def wikipedia_search(query):
    try:
        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            result = wikipedia.summary(e.options[0], sentences=2)
            return result
        except:
            return ask_ai(f"Tell me about {query} in 2 sentences")
    except:
        return ask_ai(f"Tell me about {query} in 2 sentences")

def is_open_command(command):
    # English open commands
    if command.startswith("open "):
        return True
    # Hindi open commands
    if any(word in command for word in ["kholo", "chalao", "open karo", "start karo"]):
        return True
    return False
    
    if any(keyword in command for keyword in open_keywords):
        return True
    if "kholo" in command or "chalao" in command or "open karo" in command:
        return True
    return False

def listen_for_wake_word():
    print("\n😴 Sleeping... Say 'Hey Jarvis' to activate!")
    with sd.InputStream(samplerate=SAMPLERATE, channels=1, dtype="int16", blocksize=CHUNK, device=MIC_DEVICE) as stream:
        while True:
            audio_chunk, _ = stream.read(CHUNK)
            audio_np = np.squeeze(audio_chunk)
            oww_model.predict(audio_np)
            for model_name, scores in oww_model.prediction_buffer.items():
                if scores[-1] > 0.3:
                    print("✅ Wake word detected!")
                    oww_model.prediction_buffer[model_name].clear()
                    return

# Memory se naam lo
memory = load_memory()
user_name = memory.get("name", "Lucky")

speak(f"Hello {user_name}, I am Jarvis. Say Hey Jarvis to activate me.")

while True:
    listen_for_wake_word()
    speak(f"Yes {user_name}, I am listening!")

    while True:
        command = take_command()

        if command == "":
            continue

        stop()

        print("You:", command)

        # --- Sleep ---
        if any(word in command for word in ["sleep", "so jao", "so ja"]):
            speak("Going to sleep, say Hey Jarvis to wake me up!")
            break

        # --- Exit ---
        elif any(word in command for word in ["exit", "quit", "bye", "goodbye", "band ho jao"]):
            speak(f"Goodbye {user_name}, have a great day!")
            exit()

        # --- Time ---
        elif "time" in command or "kitne baje" in command or "samay" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        # --- Date ---
        elif "date" in command or "tarikh" in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {current_date}")

        # --- Day ---
        elif "day" in command or "din" in command:
            current_day = datetime.datetime.now().strftime("%A")
            speak(f"Today is {current_day}")

        # --- Weather ---
        elif "weather" in command or "whether" in command or "mausam" in command:
            result = get_weather()
            speak(result)

        # --- Screenshot ---
        elif "screenshot" in command or "screen shot" in command or "capture" in command:
            result = take_screenshot()
            speak(result)

        # --- Battery ---
        elif "battery" in command or "charge" in command:
            result = get_battery()
            speak(result)

        # --- System Status ---
        elif "system status" in command or "cpu" in command or "ram" in command:
            result = get_system_status()
            speak(result)

        # --- Wikipedia Search ---
        elif any(word in command for word in ["who is", "what is", "tell me about", "wikipedia", "kaun hai", "kya hai", "ke baare mein"]):
            speak("Let me look that up!")
            query = command.replace("who is", "").replace("what is", "").replace("tell me about", "").replace("wikipedia", "").replace("kaun hai", "").replace("kya hai", "").replace("ke baare mein", "").strip()
            result = wikipedia_search(query)
            speak(result)

        # --- Note add karo ---
        elif "note" in command or "remember" in command or "yaad rakhna" in command or "likho" in command:
            note = command.replace("note", "").replace("remember", "").replace("yaad rakhna", "").replace("likho", "").strip()
            if note:
                add_note(note)
                speak("Got it! I have noted that")
            else:
                speak("What should I note down?")

        # --- Notes pado ---
        elif "read notes" in command or "my notes" in command or "notes batao" in command:
            notes = get_notes()
            if notes:
                speak(f"You have {len(notes)} notes.")
                for i, note in enumerate(notes):
                    speak(f"Note {i+1}: {note}")
            else:
                speak("You have no notes saved")

        # --- Summarize website ---
        elif "summarize" in command or "summary" in command:
            speak("Please tell me the website URL")
            url_command = take_command()
            if url_command:
                if "http" not in url_command:
                    url_command = "https://" + url_command
                speak("Let me read and summarize that for you")
                result = summarize_website(url_command)
                speak(result)

        # --- Cricket Score ---
        elif "cricket" in command or "match score" in command:
            speak("Let me check the cricket scores")
            result = get_cricket_score()
            speak(result)

        # --- Football Score ---
        elif "football" in command or "football score" in command:
            speak("Let me check the football scores")
            result = get_football_score()
            speak(result)

        # --- Movie Recommendations ---
        elif "movie" in command or "film" in command or "recommend" in command:
            speak("Let me think of some good movies for you")
            result = get_movie_recommendation()
            speak(result)

        # --- Joke ---
        elif "joke" in command or "funny" in command or "hasao" in command:
            if "hindi" in command:
                result = ask_ai("Tell me a funny joke in Hindi. Keep it short and natural, no bullet points.")
            else:
                result = ask_ai("Tell me a funny joke in English. Keep it short and natural.")
            speak(result)

        # --- Quote ---
        elif "quote" in command or "motivate" in command or "inspire" in command:
            result = get_quote()
            speak(result)

        # --- Coin flip ---
        elif "coin" in command or "flip" in command:
            result = flip_coin()
            speak(result)

        # --- Dice roll ---
        elif "dice" in command or "roll" in command:
            result = roll_dice()
            speak(result)

        # --- Close Apps ---
        elif "close" in command or "band karo" in command or "band kr" in command:
            result = close_app(command)
            if result:
                speak("Sure, closing it now")
            else:
                speak("Sorry, I could not find that application to close")

        # --- Lock PC ---
        elif "lock" in command or "lock karo" in command:
            speak("Locking your PC!")
            os.system("rundll32.exe user32.dll,LockWorkStation")

        # --- Volume Up ---
        elif "volume up" in command or "increase volume" in command or "awaaz badao" in command:
            set_volume("up")
            speak("Volume increased")

        # --- Volume Down ---
        elif "volume down" in command or "decrease volume" in command or "awaaz kam karo" in command:
            set_volume("down")
            speak("Volume decreased")

        # --- Mute ---
        elif "mute" in command or "chup karo" in command:
            set_volume("mute")
            speak("Muted")

        # --- Unmute ---
        elif "unmute" in command:
            set_volume("mute")
            speak("Unmuted")

        # --- Brightness Up ---
        elif "brightness up" in command or "increase brightness" in command or "roshni badao" in command:
            set_brightness(80)
            speak("Brightness increased")

        # --- Brightness Down ---
        elif "brightness down" in command or "decrease brightness" in command or "roshni kam karo" in command:
            set_brightness(30)
            speak("Brightness decreased")

        # --- Brightness Max ---
        elif "max brightness" in command:
            set_brightness(100)
            speak("Brightness set to maximum")

        # --- Brightness Min ---
        elif "min brightness" in command:
            set_brightness(10)
            speak("Brightness set to minimum")

        # --- Shutdown PC ---
        elif "shutdown pc" in command or "turn off pc" in command or "pc band karo" in command:
            speak(f"Shutting down your PC {user_name}!")
            os.system("shutdown /s /t 5")

        # --- Restart PC ---
        elif "restart pc" in command or "pc restart karo" in command:
            speak(f"Restarting your PC {user_name}!")
            os.system("shutdown /r /t 5")

        # --- Search on Google ---
        elif "search" in command and "google" in command:
            query = command.replace("search on google", "").replace("google search", "").replace("google pe search karo", "").strip()
            if query:
                speak(f"Searching {query} on Google")
                webbrowser.open(f"https://www.google.com/search?q={query}")
            else:
                speak("What should I search?")

        # --- Search on YouTube ---
        elif "search" in command and "youtube" in command:
            query = command.replace("search on youtube", "").replace("youtube search", "").replace("youtube pe search karo", "").strip()
            if query:
                speak(f"Searching {query} on YouTube")
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            else:
                speak("What should I search on YouTube?")

        # --- Open Apps ---
        elif is_open_command(command):
            result = open_app(command)
            if result:
                speak("Ji, abhi khol raha hoon!")
            else:
                speak("Sorry, I could not find that application")

        # --- Who are you ---
        elif "who are you" in command or "your name" in command or "tera naam" in command:
            speak(f"I am Jarvis, your personal AI assistant and best friend, created by {user_name}.")

        # --- How are you ---
        elif "how are you" in command or "kaisa hai" in command or "kya haal hai" in command:
            speak(f"Mast hoon {user_name} bhai, ekdum top! Tu bata kya haal hai?")

        # --- Thank you ---
        elif "thank you" in command or "thanks" in command or "shukriya" in command or "dhanyavaad" in command:
            speak("Arre yaar, mention not! Dost hain hum!")

        # --- Good morning ---
        elif "good morning" in command or "subah" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            result = get_weather()
            speak(f"Good morning {user_name}! Abhi time hai {current_time}. {result}. Aaj ka din mast raho!")

        # --- Good night ---
        elif "good night" in command or "shubh ratri" in command:
            speak(f"Good night {user_name} bhai! Kal milte hain. Sweet dreams!")

        # --- AI Fallback ---
        else:
            print("🤖 Thinking...")
            answer = ask_ai(command)
            speak(answer)