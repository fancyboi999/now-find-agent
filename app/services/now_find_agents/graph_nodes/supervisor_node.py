import json
from typing import Literal

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from loguru import logger


from app.services.now_find_agents.state_types import State


async def supervisor(state: State) -> Command[Literal["__end__"]]:
    """
    supervisor node that generate the full plan.
    监督者,监督所有任务需要用到的agent
    """
    try:
        llm = ChatOpenAI(api_key="sk-ct5qFCReZ4vsHYst5c7841D09dD84eCeA23bBfBeE5787413", base_url="https://one-api.nowcoder.com",model="gpt-4o")
        messages = state["messages"]
        # whether to enable deep thinking mode
        response = await llm.ainvoke(messages)
        return Command(goto="__end__",update={"messages": [response]})
    except Exception as e:
        logger.error(f"Error in supervisor_node: {e}")
        return Command(goto="__end__",update={"messages": [AIMessage(content=f"Error: {e}")]})