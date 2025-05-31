from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
