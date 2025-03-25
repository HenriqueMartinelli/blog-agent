# app/models/post_model.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    conteudo = Column(Text, nullable=False)
    autor = Column(String(100), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
