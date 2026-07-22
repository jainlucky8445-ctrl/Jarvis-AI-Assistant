import os
import webbrowser

def open_app(command):
    command = command.lower()

    # --- System Apps ---
    if "chrome" in command or "google" in command:
        os.system("start chrome")

    elif "edge" in command or "microsoft edge" in command:
        os.system("start msedge")

    elif "firefox" in command:
        os.system("start firefox")

    elif "notepad" in command:
        os.system("start notepad")

    elif "calculator" in command or "calc" in command or "calculator" in command:
        os.system("start calc")

    elif "paint" in command:
        os.system("start mspaint")

    elif "vs code" in command or "visual studio" in command:
        os.system("code")

    elif "file explorer" in command or "explorer" in command:
        os.system("explorer")

    elif "task manager" in command:
        os.system("taskmgr")

    elif "control panel" in command:
        os.system("control")

    elif "settings" in command:
        os.system("start ms-settings:")

    elif "camera" in command:
        os.system("start microsoft.windows.camera:")

    elif "word" in command:
        os.system("start winword")

    elif "excel" in command:
        os.system("start excel")

    elif "powerpoint" in command:
        os.system("start powerpnt")

    elif "vlc" in command:
        os.system("start vlc")

    elif "spotify" in command:
        os.system("start spotify")

    elif "discord" in command:
        os.system("start discord")

    elif "whatsapp" in command:
        os.system("start whatsapp:")

    elif "telegram" in command:
        os.system("start telegram")

    elif "cmd" in command or "command prompt" in command:
        os.system("start cmd")

    elif "powershell" in command:
        os.system("start powershell")

    # --- Websites ---
    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")

    elif "github" in command:
        webbrowser.open("https://www.github.com")

    elif "instagram" in command:
        webbrowser.open("https://www.instagram.com")

    elif "twitter" in command or "x" in command:
        webbrowser.open("https://www.twitter.com")

    elif "facebook" in command:
        webbrowser.open("https://www.facebook.com")

    elif "whatsapp web" in command:
        webbrowser.open("https://web.whatsapp.com")

    elif "chatgpt" in command:
        webbrowser.open("https://chat.openai.com")

    elif "gmail" in command:
        webbrowser.open("https://mail.google.com")

    elif "maps" in command or "google maps" in command:
        webbrowser.open("https://maps.google.com")

    elif "news" in command:
        webbrowser.open("https://news.google.com")

    else:
        return False

    return True


def close_app(command):
    command = command.lower()

    apps = {
        "chrome": "chrome.exe",
        "google": "chrome.exe",
        "edge": "msedge.exe",
        "microsoft edge": "msedge.exe",
        "firefox": "firefox.exe",
        "notepad": "notepad.exe",
        "calculator": "calculatorapp.exe",
        "calc": "calculatorapp.exe",
        "paint": "mspaint.exe",
        "vs code": "code.exe",
        "visual studio": "code.exe",
        "vlc": "vlc.exe",
        "spotify": "spotify.exe",
        "discord": "discord.exe",
        "whatsapp": "whatsapp.exe",
        "telegram": "telegram.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "task manager": "taskmgr.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
    }

    for key, exe in apps.items():
        if key in command:
            os.system(f"taskkill /f /im {exe} >nul 2>&1")
            return True

    return False