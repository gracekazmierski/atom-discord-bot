import ollama

def query_ollama(prompt):
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Atom, a Discord assistant with a sarcastic, witty personality. "
                    "Keep responses short and punchy (1–3 sentences). Avoid long monologues."
                ),
            },
            {"role": "user", "content": prompt}
        ],
        options={
            "num_predict": 600,  # Limits token output length
            "temperature": 0.8
        }
    )
    return response['message']['content']
