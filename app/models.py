from sqlalchemy import Column, Integer, String, Date, Numeric, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    telefone = Column(String(50), nullable=True)
    origem = Column(String(100), nullable=True)
    interesse = Column(String(255), nullable=True)
    renda_aproximada = Column(Integer, nullable=True)
    cidade = Column(String(100), nullable=True)
    status = Column(String(50), default="novo", nullable=False)
    score = Column(Integer, default=0, nullable=False)
    raw_payload = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())