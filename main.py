import os
from os import path
from dotenv import load_dotenv
from loguru import logger

# 加载环境变量，确保在导入任何其他模块之前加载
work_dir = os.getcwd()
env_files = [".env"]

# 强制设置DEPLOY_ENV环境变量（如果环境变量中没有，则从.env中读取ENV字段）
deploy_env = os.environ.get("DEPLOY_ENV")
if not deploy_env:
    # 尝试从.env文件中读取ENV字段
    env_path = path.join(work_dir, ".env")
    if path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('ENV='):
                    deploy_env = line.strip().split('=', 1)[1].strip()
                    # 设置环境变量，让后续代码可以使用
                    os.environ["DEPLOY_ENV"] = deploy_env
                    break

# 如果仍然没有找到，使用默认值
if not deploy_env:
    deploy_env = "dev"
    os.environ["DEPLOY_ENV"] = deploy_env

# 根据DEPLOY_ENV加载对应的环境配置文件
if deploy_env:
    env_files.append(f".env.{deploy_env}")

# 加载所有环境变量文件
for env_file in env_files:
    env_path = path.join(work_dir, env_file)
    if path.exists(env_path):
        load_dotenv(env_path)
        logger.info(f"已加载环境变量文件: {env_path}")

from uvicorn import run

from bootstrap.application import create_app
from config.config import get_settings

settings = get_settings()
app = create_app()

# 添加基础API路由
from app.api import health_router, example_router

app.include_router(health_router)
app.include_router(example_router)

# TODO: 在此处添加您的业务API路由 # [fixme]
# app.include_router(your_business_router)

# 添加根路径路由
@app.get("/")
async def root():
    return {
        "message": "FastAPI 脚手架项目",
        "version": "1.0.0",
        "docs_url": "/docs",
        "status": "running"
    }


if __name__ == "__main__":
    run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
        timeout_keep_alive=settings.UVICORN_TIMEOUT_KEEP_ALIVE,
        timeout_graceful_shutdown=settings.UVICORN_GRACEFUL_TIMEOUT,
        proxy_headers=settings.PROXY_HEADERS,
        forwarded_allow_ips=settings.FORWARDED_ALLOW_IPS,
    )
