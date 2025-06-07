import os
import ollama
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv
from atom_memory import load_memory, save_memory

# Load environment variables
load_dotenv()

OLLAMA_MODE = os.getenv("OLLAMA_MODE", "local")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
REMOTE_OLLAMA_HOST = os.getenv("OLLAMA_HOST")
ollama_client = ollama.Client(host=REMOTE_OLLAMA_HOST if OLLAMA_MODE == "remote" else None)

# Set up Ollama client
ollama_client = ollama.Client(
    host=REMOTE_OLLAMA_HOST if OLLAMA_MODE == "remote" else None
)

print(f"Using Ollama in {OLLAMA_MODE} mode with model {OLLAMA_MODEL}.")

# Logging setup
logging.basicConfig(filename=r'logs\atom.log', level=logging.INFO)

# Memory loading
memory = load_memory()
conversation_history = memory.get("conversation_history", [])
user_locations = memory.get("user_locations", {})

def log_user_activity(user_id, activity):
    logging.info(f"User {user_id} performed activity: {activity}")

def get_weather(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"It's currently {temperature}°F with {weather}."
    else:
        return "Sorry, I couldn't fetch the weather data right now."

def preprocess_prompt(prompt, lat=None, lon=None, weather_api_key=None):
    if prompt.strip().lower() in ["who is that?", "what is that?", "where is that?"]:
        if conversation_history:
            last_answer = conversation_history[-1]["content"]
            prompt = f'You just said: "{last_answer}". {prompt}'

    if "what time" in prompt.lower():
        now = datetime.now().strftime("%I:%M %p")
        prompt = f"The current time is {now}. {prompt}"

    if "weather" in prompt.lower() and lat and lon and weather_api_key:
        weather_info = get_weather(lat, lon, weather_api_key)
        prompt = f"{weather_info} {prompt}"

    return prompt

def query_ollama(prompt, lat=None, lon=None, weather_api_key=None):
    prompt = preprocess_prompt(prompt, lat, lon, weather_api_key)
    conversation_history.append({"role": "user", "content": prompt})

    response = ollama_client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are Atom, a clever and sarcastic AI assistant for Discord. You give short, punchy answers with dry humor, but you’re still helpful. If a user asks something straightforward like the time, weather, or help, answer it directly—then maybe drop a funny comment. Never be rude or avoid giving a real answer. Always be respectful, but keep it snappy and witty. If you don’t know something, just say so with a bit of sarcasm."
            },
            *conversation_history[-10:]
        ],
        options={
            "temperature": 0.5,
            "top_p": 0.9,
            "repeat_penalty": 1.1
        }
    )

    atom_reply = response["message"]["content"]
    conversation_history.append({"role": "assistant", "content": atom_reply})
    return atom_reply
