"""
Modelos Pydantic para validação de entrada/saída da API
"""
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class GastoFinanceiro(BaseModel):
    """Modelo para extração de dados financeiros"""
    categoria: Literal["Alimentação", "Transporte", "Lazer", "Saúde", "Moradia", "Outros", "Bebida"] = Field(
        description="A categoria do gasto."
    )
    meio_pagamento: Optional[Literal["Crédito", "Débito", "Refeição", "Pix"]] = Field(default=None, description="O meio de pagamento.")
    valor: float = Field(description="O valor numérico. Use ponto para decimais.")
    item: str = Field(description="Descrição curta do que foi comprado.")

    @field_validator("valor")
    def valor_positivo(cls, v):
        if v <= 0:
            raise ValueError("O valor deve ser maior que zero")
        return v


class GastoCreate(BaseModel):
    """Modelo para criação de gasto via API"""
    valor: float
    item: str
    categoria: Literal["Alimentação", "Transporte", "Lazer", "Saúde", "Moradia", "Outros", "Bebida"]
    meio_pagamento: Optional[Literal["Crédito", "Débito", "Refeição", "Pix"]] = None
    descricao_original: Optional[str] = None  # Texto original que gerou o gasto


class GastoUpdate(BaseModel):
    """Modelo para atualização de gasto via API"""
    valor: Optional[float] = None
    item: Optional[str] = None
    categoria: Optional[Literal["Alimentação", "Transporte", "Lazer", "Saúde", "Moradia", "Outros", "Bebida"]] = None
    meio_pagamento: Optional[Literal["Crédito", "Débito", "Refeição", "Pix"]] = None
    descricao_original: Optional[str] = None

    @field_validator("valor")
    def valor_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError("O valor deve ser maior que zero")
        return v


class GastoResponse(BaseModel):
    """Modelo de resposta da API com dados do gasto"""
    id: int
    valor: float
    item: str
    categoria: str
    meio_pagamento: Optional[str]
    descricao_original: Optional[str]
    data_criacao: datetime
    
    class Config:
        from_attributes = True


class ProcessamentoRequest(BaseModel):
    """Modelo para requisição de processamento de texto"""
    texto: str


class ProcessamentoResponse(BaseModel):
    """Modelo de resposta do processamento"""
    sucesso: bool
    gasto: Optional[GastoResponse] = None
    erro: Optional[str] = None
    texto_processado: Optional[str] = None

