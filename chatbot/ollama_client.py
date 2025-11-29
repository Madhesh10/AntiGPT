import os
import requests

DEEPSEEK_API_KEY = os.getenv("sk-db862d47074f4ee1bac68c9cef5da566")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


def generate_with_llm(prompt: str) -> str:
    """
    Calls DeepSeek Chat API and returns model output text.
    """
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        res = requests.post(DEEPSEEK_URL, json=payload, headers=headers, timeout=30)

        if res.status_code != 200:
            return f"[DeepSeek Error {res.status_code}: {res.text}]"

        data = res.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"[Error contacting DeepSeek API: {e}]"
