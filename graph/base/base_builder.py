from langgraph.graph import StateGraph, START, END
from typing import Optional, Dict, List
from psycopg_pool import AsyncConnectionPool
from db.pg.pg_checkpointer import AsyncCompatiblePostgresSaver
from config.env import POSTGRES_CONN_STRING


class GraphBuilder:
    """图构建器基类"""
    
    def __init__(self, state_class, config: Optional[Dict] = None):
        self.state_class = state_class
        self.config = config or {}
        self.builder = StateGraph(state_class)
        self._nodes = {}
        self._edges = []

    async def setup_checkpointer(self,):
        pool = AsyncConnectionPool(
            conninfo=POSTGRES_CONN_STRING, min_size=1, max_size=30, timeout=30
        )
        checkpointer = AsyncCompatiblePostgresSaver(pool)
        await checkpointer.setup()
        print("\033[92m✨ Checkpointer setup completed successfully! ✨\033[0m")
        return checkpointer
    
    def add_node(self, name: str, node_func, **kwargs):
        """添加节点"""
        self.builder.add_node(name, node_func)
        self._nodes[name] = {'func': node_func, 'kwargs': kwargs}
        return self
    
    def add_edge(self, from_node: str, to_node: str, condition=None):
        """添加边"""
        if condition:
            self.builder.add_conditional_edges(from_node, to_node, condition)
        else:
            self.builder.add_edge(from_node, to_node)
        self._edges.append((from_node, to_node, condition))
        return self
    
    def set_entry_point(self, node_name: str):
        """设置入口点"""
        self.builder.add_edge(START, node_name)
        return self
    
    def add_termination_edges(self, nodes: List[str]):
        """批量添加终止边"""
        for node in nodes:
            self.builder.add_edge(node, END)
        return self