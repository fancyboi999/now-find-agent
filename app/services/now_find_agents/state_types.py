from typing import Dict,List
from langgraph.graph import MessagesState


class State(MessagesState):
    """State for the agent system, extends MessagesState with next field."""
    # 基础信息

    conversation_id: str
    hr_id: str
    task_id: str
    # 任务状态
    task_status: str # PENDING, EXECUTING, COMPLETED, FAILED
    current_phase: str
    phase_progress: Dict[str, str]
    # 业务数据
    job_requirements: str
    candidate_profiles: List[Dict]
    search_results: List[Dict]
    evaluation_results: List[Dict]
    # 交互数据
    tool_calls: List[Dict]
    human_inputs: List[Dict]
    # 配置信息
    platform: str # "boss直聘", "猎聘"
    search_keywords: List[str]
    evaluation_criteria: Dict
