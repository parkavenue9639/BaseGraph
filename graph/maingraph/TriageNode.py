import asyncio
from os import name
from graph.base.BaseNode import BaseNode
from schema.graph.graph import State
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

class TriageNode(BaseNode):
    def __init__(self):
        super().__init__()

    async def __call__(self, state: State, config: RunnableConfig) -> Command:
        print(self.gemini_2.invoke("who are you"))

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
