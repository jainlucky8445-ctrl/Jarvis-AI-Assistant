from groq import Groq
import os
from dotenv import load_dotenv
from langdetect import detect
from modules.memory import load_memory, increment_conversation

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_system_prompt():
    memory = load_memory()
    name = memory.get("name", "Lucky")
    prefs = memory.get("preferences", {})
    count = memory.get("conversation_count", 0)

    return f"""You are Jarvis, a super intelligent, friendly and funny AI assistant made by {name}.
You are like a best friend — casual, fun, witty, and very helpful.
You can talk about anything — movies, cricket, life, tech, jokes, advice, anything!
You are talking via voice so keep responses natural and conversational.
Never use bullet points, markdown, or long paragraphs.
Just talk like a real dost would talk.
IMPORTANT: Always reply in the SAME language the user speaks.
If user speaks English, reply in English only.
If user speaks Hindi, reply in Hindi only.
Never mix languages unless the user does it first.
Keep responses short — max 3 sentences for simple questions.

User's name is {name}.
Total conversations so far: {count}
User preferences: {prefs}"""

conversation_history = []

def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return "en"

def detect_mood(text):
    text = text.lower()
    sad_words = ["sad", "upset", "depressed", "unhappy", "cry", "dukhi", "rona", "bura", "akela"]
    happy_words = ["happy", "great", "awesome", "excited", "khush", "mast", "zabardast", "badhiya"]
    angry_words = ["angry", "frustrated", "annoyed", "gussa", "krodh", "bakwas"]

    if any(word in text for word in sad_words):
        return "sad"
    elif any(word in text for word in happy_words):
        return "happy"
    elif any(word in text for word in angry_words):
        return "angry"
    return "neutral"

def get_mood_response(mood, name):
    if mood == "sad":
        return f"Arre {name} bhai, kya hua? Main hoon na! "
    elif mood == "happy":
        return f"Wah {name} bhai, mast hai! "
    elif mood == "angry":
        return f"Arre {name} bhai, shant ho jao! "
    return ""

def ask_ai(prompt):
    global conversation_history
    try:
        increment_conversation()

        memory = load_memory()
        name = memory.get("name", "Lucky")

        # Mood detect karo
        mood = detect_mood(prompt)
        mood_prefix = get_mood_response(mood, name)

        # Language detect karo
        lang = detect_language(prompt)

        # System prompt
        system_prompt = get_system_prompt()

        if lang == "hi":
            system_prompt += "\nUser Hindi mein bol raha hai. Sirf Hindi mein jawab do."
        else:
            system_prompt += "\nUser English mein bol raha hai. Sirf English mein jawab do."

        # History mein add karo
        conversation_history.append({
            "role": "user",
            "content": prompt
        })

        # History 20 tak limit karo
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        messages = [{"role": "system", "content": system_prompt}] + conversation_history

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=300,
            temperature=0.9
        )

        answer = response.choices[0].message.content

        # Mood prefix sirf Hindi mein add karo
        if mood_prefix and mood != "neutral" and lang == "hi":
            answer = mood_prefix + answer

        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except Exception as e:
        print("AI Error:", e)
        return "Sorry, could not process that!"