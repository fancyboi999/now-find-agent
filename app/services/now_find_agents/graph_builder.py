from langgraph.graph import StateGraph, START, END

# TODO: 开发使用内存，上生产需更换为 PostgresStore
from langgraph.checkpoint.memory import InMemorySaver

from app.services.now_find_agents.state_types import State
from app.services.now_find_agents.graph_nodes.supervisor_node import supervisor


class GraphBuilder:
    def __init__(self):
        self.store = InMemorySaver()

    async def build_graph_async(self):
        agent_builder = StateGraph(State)

        # Add nodes
        agent_builder.add_node("supervisor", supervisor)

        # Add edges
        agent_builder.add_edge(START, "supervisor")
        agent_builder.add_edge("supervisor", END)

        # Return compiled agent
        return agent_builder.compile(checkpointer=self.store)
            
