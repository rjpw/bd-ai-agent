import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MAX_CHARS = os.environ.get("MAX_CHARS")