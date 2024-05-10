from groq import AsyncGroq
import config


async def generate_from_history(history: list[dict]) -> str:
    client = AsyncGroq(api_key=config.groq_api_key)
    chat_completion = await client.chat.completions.create(messages=history, model="llama3-70b-8192", max_tokens=400)
    return chat_completion.choices[0].message.content


async def generate_single(prompt: str) -> str:
    client = AsyncGroq(api_key=config.groq_api_key)
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                           model="llama3-70b-8192", max_tokens=400)
    return chat_completion.choices[0].message.content
