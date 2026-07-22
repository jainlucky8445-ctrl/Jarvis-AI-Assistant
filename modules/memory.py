import json
import os

MEMORY_FILE = "jarvis_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {
        "name": "Lucky",
        "preferences": {},
        "notes": [],
        "conversation_count": 0
    }

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def update_preference(key, value):
    memory = load_memory()
    memory["preferences"][key] = value
    save_memory(memory)

def get_preference(key):
    memory = load_memory()
    return memory["preferences"].get(key, None)

def add_note(note):
    memory = load_memory()
    memory["notes"].append(note)
    save_memory(memory)

def get_notes():
    memory = load_memory()
    return memory["notes"]

def increment_conversation():
    memory = load_memory()
    memory["conversation_count"] += 1
    save_memory(memory)
    return memory["conversation_count"]