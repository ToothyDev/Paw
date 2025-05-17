from typing import Any

import aiohttp
from openai import AsyncOpenAI

import config
from utils.data import Fursona


async def generate_from_history(history: list[dict]) -> str:
    client = AsyncOpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)
    chat_completion = await client.chat.completions.create(messages=history, model=config.model_name)
    return _strip_thinking(chat_completion.choices[0].message.content)[:1600]


async def generate_single(prompt: str) -> str:
    client = AsyncOpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                           model=config.model_name)
    return _strip_thinking(chat_completion.choices[0].message.content)[:1600]


async def generate_sona(prompt: str) -> Fursona:
    client = AsyncOpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                           model=config.model_name,
                                                           response_format={"type": "json_object"})
    return Fursona.model_validate_json(chat_completion.choices[0].message.content)


async def apireq(url, headers=None, data=None) -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, json=data) as response:
            return await response.json()


def _strip_thinking(response: str) -> str:
    """ Strips thinking parts from reasoning model outputs, at least from Groq. Changes nothing for regular models """
    return response.split("</think>")[-1].strip()
