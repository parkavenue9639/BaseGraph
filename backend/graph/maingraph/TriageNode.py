import asyncio
import logging
from os import name
from graph.base.BaseNode import BaseNode
from schema.graph.graph import State
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from langgraph.graph import END

logger = logging.getLogger(__name__)

class TriageNode(BaseNode):
    def __init__(self):
        super().__init__()

    async def __call__(self, state: State, config: RunnableConfig) -> Command:
        # 使用异步流式调用，让 LangGraph 的 astream_events 能够实时捕获流式事件
        messages = state.get("messages", [])
        if messages:
            # 使用 ainvoke 异步调用，不会阻塞流式事件
            response = await self.gemini_2.ainvoke(messages)
            logger.info(f"Triage response: {response.content}")
        return Command(goto=END)

_triage_node_instance = TriageNode()

async def triage_node(state: State, config: RunnableConfig) -> Command:
    return await _triage_node_instance(state, config)

if __name__ == "__main__":
    async def main():
        state = State()
        config = RunnableConfig()
        result = await triage_node(state, config)
        return result
    
    asyncio.run(main())
