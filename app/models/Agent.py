from sqlalchemy import Boolean, Column, Integer, String, Text

from .BaseModels import Base, TimeCreated


class Agent(Base, TimeCreated):
    __tablename__ = "agent"

    id = Column(
        Integer,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        comment="agent id",
    )
    name = Column(
        String(256), unique=True, nullable=False, index=True, comment="agent 名称"
    )
    description = Column(String(256), nullable=False, comment="agent 描述")
    status = Column(Integer, nullable=False, comment="agent 状态")
    prompt = Column(Text, nullable=False, comment="agent 提示词")
    bind_tools_list = Column(String(256), nullable=False, comment="agent 绑定的工具")
    agent_model_id = Column(Integer, nullable=False, comment="agent 使用的 llm 模型")
    zh_name = Column(String(256), nullable=True, comment="agent 中文名称")
    is_optional = Column(Boolean, nullable=False, default=False, comment="是否可选")
    level = Column(Integer, nullable=False, comment="agent 级别")
