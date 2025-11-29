# chatbot/ollama_client.py
import os
import requests

DEEPSEEK_API_KEY = os.getenv("sk-db862d47074f4ee1bac68c9cef5da566")

def generate_with_llm(prompt):
    if not DEEPSEEK_API_KEY:
        return "[DeepSeek API key missing]"

    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return f"[DeepSeek Error {response.status_code}: {response.text}]"

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"[DeepSeek Exception: {e}]"
