from typing import Any


def create_workflow_config(task_id: str, **additional_config) -> dict[str, Any]:
    """创建工作流配置"""
    config = {"configurable": {"thread_id": task_id, "task_id": task_id, **additional_config}}
    return config