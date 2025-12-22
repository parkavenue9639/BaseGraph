from langchain_openai import ChatOpenAI
from config.env import GEMINI_2_5_FLASH_API_KEY, GEMINI_2_5_FLASH_BASE_URL, GEMINI_2_5_FLASH_MODEL

class LLMSelector:
    def __init__(self, ):
        pass

    def get_llm_by_name(self, name: str):
        if name == "gemini-2.5-flash":
            if not GEMINI_2_5_FLASH_API_KEY:
                raise ValueError("GEMINI_2_5_FLASH_API_KEY 未设置，请检查 .env 文件")
            if not GEMINI_2_5_FLASH_BASE_URL:
                raise ValueError("GEMINI_2_5_FLASH_BASE_URL 未设置，请检查 .env 文件")
            if not GEMINI_2_5_FLASH_MODEL:
                raise ValueError("GEMINI_2_5_FLASH_MODEL 未设置，请检查 .env 文件")
            
            return self.create_openai_llm(GEMINI_2_5_FLASH_MODEL, GEMINI_2_5_FLASH_BASE_URL, GEMINI_2_5_FLASH_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM: {name}")

    def create_openai_llm(self, model: str, base_url: str, api_key: str, temperature: float = 0.0, **kwargs):
        llm_kwargs = {
            "model": model,
            "temperature": temperature,
            **kwargs
        }
        
        # 确保 base_url 和 api_key 被正确设置
        if base_url:
            llm_kwargs["base_url"] = base_url
        if api_key:
            llm_kwargs["api_key"] = api_key

        return ChatOpenAI(**llm_kwargs)