import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gemini-3.5-flash-lite")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
LLM_API_KEY = os.environ["LLM_API_KEY"]

CROSSMARK = os.getenv("CROSSMARK", "❌")
CONFUSED = os.getenv("CROSSMARK", "😕")
