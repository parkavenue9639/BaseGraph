from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_2_5_FLASH_API_KEY = os.getenv("GEMINI_2_5_FLASH_API_KEY")
GEMINI_2_5_FLASH_BASE_URL = os.getenv("GEMINI_2_5_FLASH_BASE_URL")
GEMINI_2_5_FLASH_MODEL = os.getenv("GEMINI_2_5_FLASH_MODEL")