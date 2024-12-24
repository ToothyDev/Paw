import aiohttp
from groq import AsyncGroq as AI

import config
from utils.data import Fursona

def get_client() -> tuple[AI, str, str]:
    """Returns the AsyncGroq client and the language and vision model names.
    Works with both OpenAI and Groq API keys interchangeably without any changes to the code.
    """
    api_key = config.ai_api_key
    if api_key.startswith("sk-"):
        return (
            AI (
                api_key=api_key,
                base_url="https://api.openai.com/v1"
            ), # Client using OpenAI API
            # You can switch these to other models if you want to, I just just set them to the mini model because it's cheaper and honestly, it's good enough for most use cases
            "gpt-4o-mini-2024-07-18", # Language model
            "gpt-4o-mini-2024-07-18" # Vision model
            )
    elif api_key.startswith("gsk_"):
        return (
            AI (
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            ), # Client, using Groq API
            "llama-3.3-70b-versatile", # Language model
            "llama-3.2-11b-vision-preview" # Vision model, you can change this to "llama-3.2-90b-vision-preview" if you want to, but It'll be slower
            )
    else:
        raise ValueError("Invalid API key. Please provide a valid OpenAI/Groq API key.")

async def generate_from_history(history: list[dict]) -> str:
    client, language_model, vision_model = get_client()
    chat_completion = await client.chat.completions.create(messages=history, model=language_model,
                                                        max_tokens=400)
    return chat_completion.choices[0].message.content


async def analyse_image(image_url: str) -> str:
    client, language_model, vision_model = get_client()
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
        model=vision_model,
    )
    return image_completion.choices[0].message.content

async def generate_single(prompt: str) -> str: # For future me, this is never used as of 2024-12-21 YYYY-MM-DD
    client, language_model, vision_model = get_client()
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                        model=language_model, max_tokens=400)
    return chat_completion.choices[0].message.content


async def generate_sona(prompt: str) -> Fursona:
    client, language_model, vision_model = get_client()
    chat_completion = await client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                        model=language_model,
                                                        response_format={"type": "json_object"})
    return Fursona.model_validate_json(chat_completion.choices[0].message.content)


async def apireq(url, headers=None, data=None) -> dict[str, any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, json=data) as response:
            return await response.json()

def is_ai_enabled() -> bool:
    if config.ai_api_key.startswith("sk-") or config.ai_api_key.startswith("gsk_"):
        return True
    else:
        return False
