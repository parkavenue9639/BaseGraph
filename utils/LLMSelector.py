from langchain_openai import ChatOpenAI
from config.env import GEMINI_2_5_FLASH_API_KEY, GEMINI_2_5_FLASH_BASE_URL, GEMINI_2_5_FLASH_MODEL

class LLMSelector:
    def __init__(self, ):
        pass

    def get_llm_by_name(self, name: str):
        if name == "gemini-2.5-flash":
            return self.create_openai_llm(GEMINI_2_5_FLASH_MODEL, GEMINI_2_5_FLASH_BASE_URL, GEMINI_2_5_FLASH_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM: {name}")

    def create_openai_llm(self, model: str, base_url: str, api_key: str, temperature: float = 0.0, **kwargs):
        llm_kwargs = {
            "model": model,
            "base_url": base_url,
            "api_key": api_key,
            "temperature": temperature,
            **kwargs
        }
        
        if base_url:
            llm_kwargs["base_url"] = base_url
        if api_key:
            llm_kwargs["api_key"] = api_key

        return ChatOpenAI(**llm_kwargs)