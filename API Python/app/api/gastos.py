"""
Rotas CRUD de gastos financeiros
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.models import get_db, Gasto
from app.models.schemas import GastoCreate, GastoUpdate, GastoResponse

router = APIRouter()


@router.post("/gastos", response_model=GastoResponse)
async def criar_gasto(
    gasto: GastoCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um gasto diretamente no banco de dados (sem processamento de LLM)
    """
    try:
        gasto_db = Gasto(
            valor=gasto.valor,
            item=gasto.item,
            categoria=gasto.categoria,
            meio_pagamento=gasto.meio_pagamento,
            descricao_original=gasto.descricao_original
        )
        
        db.add(gasto_db)
        db.commit()
        db.refresh(gasto_db)
        
        return GastoResponse(
            id=gasto_db.id,
            valor=gasto_db.valor,
            item=gasto_db.item,
            categoria=gasto_db.categoria,
            meio_pagamento=gasto_db.meio_pagamento,
            descricao_original=gasto_db.descricao_original,
            data_criacao=gasto_db.data_criacao
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/gastos", response_model=List[GastoResponse])
async def listar_gastos(
    skip: int = 0,
    limit: int = 40,
    db: Session = Depends(get_db)
):
    """
    Lista todos os gastos cadastrados
    """
    gastos = db.query(Gasto).order_by(Gasto.data_criacao.desc()).offset(skip).limit(limit).all()
    return [
        GastoResponse(
            id=gasto.id,
            valor=gasto.valor,
            item=gasto.item,
            categoria=gasto.categoria,
            meio_pagamento=gasto.meio_pagamento,
            descricao_original=gasto.descricao_original,
            data_criacao=gasto.data_criacao
        )
        for gasto in gastos
    ]


@router.get("/gastos/{gasto_id}", response_model=GastoResponse)
async def obter_gasto(
    gasto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém um gasto específico por ID
    """
    gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
    
    return GastoResponse(
        id=gasto.id,
        valor=gasto.valor,
        item=gasto.item,
        categoria=gasto.categoria,
        meio_pagamento=gasto.meio_pagamento,
        descricao_original=gasto.descricao_original,
        data_criacao=gasto.data_criacao
    )


@router.put("/gastos/{gasto_id}", response_model=GastoResponse)
async def atualizar_gasto(
    gasto_id: int,
    gasto_update: GastoUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um gasto existente
    """
    gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
    
    try:
        # Atualiza apenas os campos fornecidos
        if gasto_update.valor is not None:
            if gasto_update.valor <= 0:
                raise HTTPException(status_code=400, detail="O valor deve ser maior que zero")
            gasto.valor = gasto_update.valor
        
        if gasto_update.item is not None:
            gasto.item = gasto_update.item
        
        if gasto_update.categoria is not None:
            gasto.categoria = gasto_update.categoria

        if gasto_update.meio_pagamento is not None:
            gasto.meio_pagamento = gasto_update.meio_pagamento
        
        if gasto_update.descricao_original is not None:
            gasto.descricao_original = gasto_update.descricao_original
        
        db.commit()
        db.refresh(gasto)
        
        return GastoResponse(
            id=gasto.id,
            valor=gasto.valor,
            item=gasto.item,
            categoria=gasto.categoria,
            meio_pagamento=gasto.meio_pagamento,
            descricao_original=gasto.descricao_original,
            data_criacao=gasto.data_criacao
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/gastos/{gasto_id}")
async def deletar_gasto(
    gasto_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um gasto por ID
    """
    gasto = db.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
    
    db.delete(gasto)
    db.commit()
    
    return {"mensagem": "Gasto deletado com sucesso"}

