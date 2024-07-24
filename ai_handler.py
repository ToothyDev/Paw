from groq import AsyncGroq
import config
from utils import Fursona


async def generate_from_history(history: list[dict]) -> str:
    client = AsyncGroq(api_key=config.groq_api_key)
    chat_completion = await client.chat.completions.create(messages=history, model="llama-3.1-70b-versatile",
                                                           max_tokens=400)
    return chat_completion.choices[0].message.content


async def generate_single(prompt: str) -> str:
    client = AsyncGroq(api_key=config.groq_api_key)
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                           model="llama-3.1-70b-versatile", max_tokens=400)
    return chat_completion.choices[0].message.content


async def generate_sona(prompt: str) -> Fursona:
    client = AsyncGroq(api_key=config.groq_api_key)
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                           model="llama-3.1-70b-versatile",
                                                           response_format={"type": "json_object"})
    return Fursona.model_validate_json(chat_completion.choices[0].message.content)
