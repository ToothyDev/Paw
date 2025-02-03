import base64

import aiohttp
from openai import AsyncOpenAI

import config
from utils.data import Fursona


async def generate_from_history(history: list[dict]) -> str:
    client = AsyncOpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)
    chat_completion = await client.chat.completions.create(messages=history, model=config.text_model)
    return _strip_thinking(chat_completion.choices[0].message.content)[:1600]


# Only needed for Groq anymore, Gemini and OpenAI can do handle sysprompt + multiple images per message fine
# Can be removed if Groq fixes their stuff, or if Groq compatibility is removed
async def analyse_image(image_bytes: bytes) -> str:
    client = AsyncOpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Describe this image. Your output will be used to describe this image to a 'blind' LLM. "
                             "Summarise in one or maximum two sentences."
                     },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    },
                ],
            }
        ],
        model=config.vision_model,
    )
    return image_completion.choices[0].message.content


async def generate_single(prompt: str) -> str:
    client = AsyncOpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                           model=config.text_model)
    return _strip_thinking(chat_completion.choices[0].message.content)[:1600]


async def generate_sona(prompt: str) -> Fursona:
    client = AsyncOpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                           model=config.text_model,
                                                           response_format={"type": "json_object"})
    return Fursona.model_validate_json(chat_completion.choices[0].message.content)


async def apireq(url, headers=None, data=None) -> dict[str, any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, json=data) as response:
            return await response.json()


def _strip_thinking(response: str) -> str:
    """ Strips thinking parts from reasoning model outputs, at least from Groq. Changes nothing for regular models"""
    if "</think>" in response:
        response = response.split("</think>", 1)[-1].strip()
    return response
