import os
from openai import OpenAI


def get_ai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url)


def generate_chat_reply(message: str) -> str:
    client = get_ai_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}],
    )
    return response.choices[0].message.content or ""
