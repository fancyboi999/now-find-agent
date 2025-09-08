import asyncio
from app.services.workflow.start_workflow import run_agent_workflow

if __name__ == "__main__":
    asyncio.run(run_agent_workflow(user_input="请帮我在boss直聘寻找运营经理候选人，目标是每日找到4个匹配候选人并加入收藏夹", hr_id=1))