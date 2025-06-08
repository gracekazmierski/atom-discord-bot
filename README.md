# Atom Discord Bot

**Atom** is a modular, customizable Discord bot designed for task management, user interaction, and seamless integration with external services. It features a flexible plugin architecture and includes capabilities like chat processing, note-taking, admin commands, and alert handling.

## 🚀 Features

- 📌 Modular Cog system (`admin`, `chat`, `alerts`, `tasks`, `notes`)
- 📂 Persistent user data management
- 💬 AI chat integration with Ollama (`ollama_client.py`)
- 🧠 Session and memory handling for stateful interactions
- 🛠️ Admin tools for server management
- 🔔 Alert and task scheduling
- 🧪 Ready for deployment on cloud platforms with `Procfile` and `Modelfile`

## 📁 Project Structure

```
atom-discord-bot/
├── bot.py                  # Main bot entry point
├── config.py               # Configuration settings
├── memory.py               # In-memory session store
├── ollama_client.py        # Integration with AI model (e.g. Ollama)
├── session_manager.py      # Manages sessions across users
├── user_data.py            # Persistent user data handling
├── requirements.txt        # Python dependencies
├── Procfile                # For deployment (e.g. Heroku)
├── Modelfile               # For model-based deployment tools
├── cogs/                   # Cog modules for bot functionality
│   ├── admin.py
│   ├── alerts.py
│   ├── chat.py
│   ├── notes.py
│   └── tasks.py
└── README.md               # This file
```

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/atom-discord-bot.git
   cd atom-discord-bot
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your `.env` or `config.py` with your Discord bot token and necessary settings.

## 🧪 Running the Bot

```bash
python bot.py
```

To run with a process manager like [foreman](https://github.com/ddollar/foreman):

```bash
foreman start
```

## 🧩 Extending Functionality

Add new commands by creating cog modules under the `cogs/` directory. Example structure:

```python
# cogs/example.py
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello from Atom!")

def setup(bot):
    bot.add_cog(Example(bot))
```

## 🧠 AI Chat

The `ollama_client.py` allows interaction with a local or remote AI model. Make sure to set up your model endpoint in the configuration.

## 🛡️ License

MIT License. See `LICENSE` file for details.

## 🙌 Credits

Developed by **Grace Kazmierski**  
Inspired by modular Discord bot designs and integrated AI assistants.
