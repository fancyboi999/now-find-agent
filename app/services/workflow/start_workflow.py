import argparse
import asyncio

from loguru import logger

from app.services.now_find_agents.graph_builder import GraphBuilder
from app.services.workflow.base import create_workflow_config
from app.utils.common.id_util import IdUtil


async def run_agent_workflow(
    user_input: str,
    hr_id: int,
):
    if not user_input:
        raise ValueError("Input could not be empty")

    # 确保图已初始化
    graph = await GraphBuilder().build_graph_async()

    # 为会话创建唯一ID (用于checkpointer)
    task_id = IdUtil.generate_uuid_32()
    logger.info(f"创建新会话,task_id: {task_id}")

    # 初始化创建任务表数据
    data = {
        "task_id": task_id,
        "conversation_id": task_id,
        "messages": [{"role": "user", "content": user_input}],
        "hr_id": hr_id,
        "task_status": "PENDING",
        "current_phase": "PENDING",
        "phase_progress": {},
        "job_requirements": user_input,
        "candidate_profiles": [],
        "search_results": [],
        "evaluation_results": [],
        "tool_calls": [],
        "human_inputs": [],
        "platform": "boss直聘",
        "search_keywords": [],
        "evaluation_criteria": {},
    }


    # 创建config配置
    config = create_workflow_config(task_id = task_id,)

    # 运行工作流
    stream_generator = graph.astream(data, config=config,stream_mode = ["values","updates","messages"])
    async for event in stream_generator:
        print(f"event: {event}\n")

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="运行Agent工作流")
    parser.add_argument(
        "--input",
        type=str,
        default="不要搜索,直接做菜的精髓口播稿,300字",
        help="用户输入文本",
    )
    parser.add_argument(
        "--hr_id",
        type=int,
        default=1,
        help="HR ID",
    )
    # 解析命令行参数
    args = parser.parse_args()

    # 运行工作流
    asyncio.run(run_agent_workflow(args.input, args.hr_id))
