import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Cricket score - no API needed
def get_cricket_score():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(
            "https://www.cricbuzz.com/cricket-match/live-scores",
            headers=headers,
            timeout=5
        )
        from html.parser import HTMLParser

        class ScoreParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.scores = []
                self.capture = False

            def handle_starttag(self, tag, attrs):
                attrs_dict = dict(attrs)
                if "class" in attrs_dict and "cb-lv-scrs-col" in attrs_dict["class"]:
                    self.capture = True

            def handle_endtag(self, tag):
                self.capture = False

            def handle_data(self, data):
                if self.capture and data.strip():
                    self.scores.append(data.strip())

        parser = ScoreParser()
        parser.feed(response.text)

        if parser.scores:
            return f"Live cricket: {', '.join(parser.scores[:4])}"
        else:
            return "No live cricket matches right now"
    except:
        return "Could not fetch cricket score right now"

# Football score
def get_football_score():
    try:
        api_key = os.getenv("FOOTBALL_API_KEY")
        if not api_key:
            return "Football API key not set"
        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": api_key}
        response = requests.get(url, headers=headers)
        data = response.json()

        matches = data.get("matches", [])
        if matches:
            match = matches[0]
            home = match["homeTeam"]["name"]
            away = match["awayTeam"]["name"]
            status = match["status"]
            home_score = match["score"]["fullTime"]["home"]
            away_score = match["score"]["fullTime"]["away"]
            if home_score is not None:
                return f"{home} {home_score} vs {away} {away_score}"
            else:
                return f"{home} vs {away}, status: {status}"
        else:
            return "No football matches right now"
    except:
        return "Could not fetch football score"

# Movie recommendations - AI se
def get_movie_recommendation():
    from modules.ai import ask_ai
    return ask_ai("Recommend 3 popular movies right now in one sentence each, no bullet points")

# Joke - no API needed
def get_joke():
    try:
        response = requests.get(
            "https://official-joke-api.appspot.com/random_joke",
            timeout=5
        )
        data = response.json()
        return f"{data['setup']} ... {data['punchline']}"
    except:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "I told my computer I needed a break. Now it won't stop sending me Kit Kat ads.",
            "Why was the math book sad? Because it had too many problems!"
        ]
        return random.choice(jokes)

# Motivational quote - no API needed
def get_quote():
    try:
        response = requests.get(
            "https://zenquotes.io/api/random",
            timeout=5
        )
        data = response.json()
        return f"{data[0]['q']} by {data[0]['a']}"
    except:
        quotes = [
            "Believe in yourself and all that you are!",
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Success is not final, failure is not fatal. - Winston Churchill",
            "Don't watch the clock, do what it does. Keep going. - Sam Levenson"
        ]
        return random.choice(quotes)

# Coin flip
def flip_coin():
    return f"It's {random.choice(['Heads', 'Tails'])}!"

# Dice roll
def roll_dice():
    return f"You rolled a {random.randint(1, 6)}!"