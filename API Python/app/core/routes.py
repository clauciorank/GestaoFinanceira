"""
Rotas principais da aplicação (root, health, etc.)
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.config import settings
import os

router = APIRouter()


@router.get("/")
async def root():
    """Rota raiz - redireciona para a interface web"""
    html_path = os.path.join(os.path.dirname(__file__), "..", "..", "templates", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    return {
        "mensagem": "Gestor Financeiro API",
        "docs": "/docs",
        "status": "online"
    }


@router.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "whisper_mode": settings.WHISPER_MODE,
        "llm_mode": settings.LLM_MODE
    }

