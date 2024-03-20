import discord
import google.generativeai as genai

import config


async def generate(prompt: str):
    genai.configure(api_key=config.api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = await model.generate_content_async(prompt)
    return response.text


async def generate_stream(ctx: discord.ApplicationContext, prompt: str):
    genai.configure(api_key=config.api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = await model.generate_content_async(prompt, stream=True)
    edited = False
    text = ""
    async for chunk in response:
        if edited:
            text += chunk.text
            await ctx.edit(content=text)
        else:
            text += chunk.text
            await ctx.respond(text)
            edited = True
