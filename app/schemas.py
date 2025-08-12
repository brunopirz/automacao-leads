from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LeadCreate(BaseModel):
    nome: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    origem: Optional[str]
    interesse: Optional[str]
    renda_aproximada: Optional[int]
    cidade: Optional[str]
    raw_payload: Optional[dict] = None

class LeadUpdate(BaseModel):
    nome: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    origem: Optional[str]
    interesse: Optional[str]
    renda_aproximada: Optional[int]
    cidade: Optional[str]
    status: Optional[str]
    score: Optional[int]

class LeadOut(BaseModel):
    id: int
    nome: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    origem: Optional[str]
    interesse: Optional[str]
    renda_aproximada: Optional[int]
    cidade: Optional[str]
    status: str
    score: int
    raw_payload: Optional[dict]
    created_at: datetime

    class Config:
        orm_mode = True