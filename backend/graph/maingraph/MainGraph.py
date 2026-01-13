from graph.base.base_builder import GraphBuilder
from typing import Optional, Dict
from schema.graph.graph import State
from langgraph.graph import START, END
from graph.maingraph.TriageNode import triage_node
class MainGraphBuilder(GraphBuilder):

    def __init__(self, config:Optional[Dict] = None):
        super().__init__(State, config)
        self._setup_nodes()
        self._setup_edges()

    async def build_graph(self, recursion_limit: Optional[int] = None):
        checkpointer = await self.setup_checkpointer()
        graph = self.builder.compile(checkpointer=checkpointer)
        if recursion_limit:
            graph.config = graph.config or {}
            graph.config["recursion_limit"] = recursion_limit
        
        return graph

    # -------inner method--------

    def _setup_nodes(self):
        self.builder.add_node("triage", triage_node)

    def _setup_edges(self):
        self.builder.add_edge(START, "triage")
        self.builder.add_edge("triage", END)