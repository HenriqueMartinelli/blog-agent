from datetime import datetime
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    titulo: str = Field(..., example="5 tendências de IA em 2025")
    conteudo: str = Field(..., example="A inteligência artificial continua...")
    autor: str = Field(..., example="Agente Autônomo")

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    data_criacao: datetime

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    id: int
    titulo: str
    conteudo: str
    autor: str
    data_criacao: datetime

    class Config:
        from_attributes = True 

class ErrorMessage(BaseModel):
    detail: str