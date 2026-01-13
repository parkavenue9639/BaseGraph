from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langgraph.types import Command
from langchain_core.runnables import RunnableConfig
from schema.graph.graph import State
from utils.LLMSelector import LLMSelector

llm_selector = LLMSelector()


class BaseNode(ABC):
    def __init__(self):
        self.gemini_2 = llm_selector.get_llm_by_name("gemini-2.5-flash")

    @abstractmethod
    async def __call__(self, state: State, config: RunnableConfig) -> Command:
        pass