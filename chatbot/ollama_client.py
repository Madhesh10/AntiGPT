# chatbot/ollama_client.py
import os
import requests
from typing import Optional

# read the API key from an environment variable (exact name below)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# DeepSeek endpoint (confirm docs if different)
DEESEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def _extract_text_from_response(data: dict) -> Optional[str]:
    """
    Try several ways to extract a text reply from DeepSeek's JSON response.
    Returns the text or None if not found.
    """
    try:
        # typical chat shape: choices[0].message.content
        choices = data.get("choices") or []
        if choices and isinstance(choices, list):
            c0 = choices[0]
            if isinstance(c0, dict):
                # look for chat/message/content
                message = c0.get("message") or c0.get("delta") or {}
                if isinstance(message, dict):
                    content = message.get("content")
                    if content:
                        return content
                # or direct text field
                text = c0.get("text") or c0.get("content")
                if text:
                    return text
        # fallback: maybe response.top_level_text or data['output']
        for k in ("output", "text", "message"):
            v = data.get(k)
            if isinstance(v, str) and v.strip():
                return v
    except Exception:
        pass
    return None

def generate_with_llm(prompt: str, model: str = "deepseek-chat") -> str:
    """
    Call DeepSeek and return assistant text, or a helpful error string.
    """
    if not DEEPSEEK_API_KEY:
        return "[DeepSeek API key missing]"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        # Add other params if you want (temperature, max_tokens) per DeepSeek docs
    }

    try:
        resp = requests.post(DEESEEK_URL, headers=headers, json=payload, timeout=30)
    except requests.RequestException as e:
        return f"[DeepSeek RequestException: {e}]"

    # helpful debug information on non-200
    if resp.status_code == 401:
        return "[DeepSeek Error 401: Authentication failed — check DEEPSEEK_API_KEY]"
    if resp.status_code >= 400:
        # include server body for debugging (shorten if very long)
        text = resp.text
        return f"[DeepSeek Error {resp.status_code}: {text}]"

    # parse JSON and extract text safely
    try:
        data = resp.json()
    except Exception as e:
        return f"[DeepSeek JSON parse error: {e}]"

    text = _extract_text_from_response(data)
    if text:
        return text.strip()

    # fallback: return the JSON as a string for debugging
    return f"[DeepSeek returned unexpected JSON: {data}]"
