"""
Configuração e criação da aplicação FastAPI
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.models import init_db
import os


def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI
    """
    # Inicializa o banco de dados
    init_db()
    
    # Cria a aplicação FastAPI
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description=settings.API_DESCRIPTION
    )
    
    # Configura CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Em produção, especifique os domínios permitidos
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Middleware para tratar requisições HTTP quando HTTPS está habilitado
    @app.middleware("http")
    async def https_redirect_middleware(request: Request, call_next):
        if settings.USE_HTTPS:
            # Se receber requisição HTTP, retorna erro explicativo
            if request.url.scheme == "http":
                return JSONResponse(
                    status_code=400,
                    content={
                        "erro": "HTTPS requerido",
                        "mensagem": "Esta aplicação está configurada para HTTPS. Acesse via https://",
                        "url_correta": str(request.url).replace("http://", "https://")
                    }
                )
        return await call_next(request)
    
    # Serve arquivos estáticos (se existirem)
    static_dir = os.path.join(os.path.dirname(__file__), "..", "..", "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    return app

