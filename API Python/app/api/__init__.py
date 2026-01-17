"""
Agrupa todos os routers da API
"""
from fastapi import APIRouter
from app.api import processamento, gastos

# Router principal que agrupa todos os routers
api_router = APIRouter()

# Inclui os routers específicos
api_router.include_router(
    processamento.router,
    tags=["Processamento"]
)

api_router.include_router(
    gastos.router,
    tags=["Gastos"]
)
