"""
Ponto de entrada da aplicação
"""
from app.core.app import create_app
from app.core.routes import router as core_router
from app.api import api_router

# Cria a aplicação
app = create_app()

# Inclui as rotas principais
app.include_router(core_router)

# Inclui as rotas da API
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
