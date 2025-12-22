from dotenv import load_dotenv
import os
from pathlib import Path

# 获取项目根目录（config 目录的父目录）
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"

# 明确指定 .env 文件路径
env_loaded = load_dotenv(dotenv_path=env_file)

# 调试信息
if not env_loaded:
    print(f"[WARNING] .env 文件未找到或未加载: {env_file}")

GEMINI_2_5_FLASH_API_KEY = os.getenv("GEMINI_2_5_FLASH_API_KEY")
GEMINI_2_5_FLASH_BASE_URL = os.getenv("GEMINI_2_5_FLASH_BASE_URL")
GEMINI_2_5_FLASH_MODEL = os.getenv("GEMINI_2_5_FLASH_MODEL")

POSTGRES_CONN_STRING = os.getenv("POSTGRES_CONN_STRING")