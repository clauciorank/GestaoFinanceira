"""
Modelos de banco de dados (ORM)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import settings

Base = declarative_base()


class Gasto(Base):
    """Modelo de tabela para gastos financeiros"""
    __tablename__ = "gastos"
    
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    item = Column(String(255), nullable=False)
    categoria = Column(String(50), nullable=False)
    meio_pagamento = Column(String(50), nullable=True)
    descricao_original = Column(Text, nullable=True)  # Texto original que gerou o gasto
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)


# Configuração do banco de dados
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Inicializa o banco de dados criando as tabelas"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

