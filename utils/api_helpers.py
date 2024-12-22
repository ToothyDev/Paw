import aiohttp
from groq import AsyncGroq

import config
from utils.data import Fursona


async def generate_from_history(history: list[dict]) -> str:
    client = AsyncGroq(api_key=config.groq_api_key)
    chat_completion = await client.chat.completions.create(messages=history, model=config.text_model,
                                                           max_tokens=400)
    return chat_completion.choices[0].message.content


async def analyse_image(image_url: str) -> str:
    client = AsyncGroq(api_key=config.groq_api_key)
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
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        model=config.vision_model,
    )
    return image_completion.choices[0].message.content


async def generate_single(prompt: str) -> str:
    client = AsyncGroq(api_key=config.groq_api_key)
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                           model=config.text_model, max_tokens=400)
    return chat_completion.choices[0].message.content


async def generate_sona(prompt: str) -> Fursona:
    client = AsyncGroq(api_key=config.groq_api_key)
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                           model=config.text_model,
                                                           response_format={"type": "json_object"})
    return Fursona.model_validate_json(chat_completion.choices[0].message.content)


async def apireq(url, headers=None, data=None) -> dict[str, any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, json=data) as response:
            return await response.json()
