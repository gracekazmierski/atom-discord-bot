import ollama
from datetime import datetime
import requests
import logging

logging.basicConfig(filename=r'logs\atom.log', level=logging.INFO)

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

def preprocess_prompt(prompt):
    if "what time" in prompt.lower():
        now = datetime.now().strftime("%I:%M %p")
        prompt = f"The current time is {now}. {prompt}"
    return prompt


conversation_history = [
    {
        "role": "system",
        "content": (
            "You are Atom, a sarcastic but helpful AI assistant with dry humor. "
            "You're clever, respectful, and always get to the point. Never ramble. "
            "Use short, punchy replies. You're fine dropping a snarky comment, "
            "but you're never mean. Keep it fun, keep it sharp. Do 10% sarcasm, 90% helpfulness. "
        )
    }
]

def query_ollama(prompt):
    prompt = preprocess_prompt(prompt)
    conversation_history.append({
        "role": "user",
        "content": prompt
    })

    # Query Ollama with full history
    response = ollama.chat(
        model="llama3",
        messages=conversation_history,
        options={
            "num_predict": 400,
            "temperature": 0.8
        }
    )

    # Append Atom's reply to the history
    atom_reply = response["message"]["content"]
    conversation_history.append({
        "role": "assistant",
        "content": atom_reply
    })

    return atom_reply
