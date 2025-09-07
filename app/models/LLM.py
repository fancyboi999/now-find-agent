from sqlalchemy import Column, Integer, String

from .BaseModels import Base, TimeCreated


class LLM(Base, TimeCreated):
    __tablename__ = "llm"

    id = Column(
        Integer,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        comment="llm id",
    )
    provider = Column(String(256), nullable=False, comment="llm 提供商")
    model_name = Column(String(256), nullable=False, comment="llm 模型名称")
    model_type = Column(
        String(256),
        nullable=False,
        comment="llm 模型类型,1: basic模型, 2: 思考模型, 3: 多模态模型",
    )
    api_key = Column(String(256), nullable=False, comment="llm 模型 api key")
    api_url = Column(String(256), nullable=False, comment="llm 模型 api url")
    status = Column(Integer, nullable=False, comment="llm 模型状态")
