"""
Configurações da aplicação
Facilita a troca entre modelos locais e APIs originais
"""
import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configurações centralizadas da aplicação"""
    
    # Configurações do Whisper
    WHISPER_MODE: Literal["local", "api"] = os.getenv("WHISPER_MODE", "local")
    WHISPER_URL: str = os.getenv("WHISPER_URL", "http://localhost:8000/transcribe")
    
    # Configurações do LLM
    LLM_MODE: Literal["local", "api"] = os.getenv("LLM_MODE", "local")
    LLM_URL: str = os.getenv("LLM_URL", "http://localhost:8002/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "neuralmagic/Llama-3.2-3B-Instruct-quantized.w8a8")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "EMPTY")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "EMPTY")
    
    # Configurações do Banco de Dados
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./gestor_financeiro.db")
    
    # Configurações da API
    API_TITLE: str = "Gestor Financeiro API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API para gestão financeira com processamento de texto e áudio"
    
    # Configurações de SSL/HTTPS
    USE_HTTPS: bool = os.getenv("USE_HTTPS", "false").lower() == "true"
    SSL_CERT_FILE: str = os.getenv("SSL_CERT_FILE", "certs/cert.pem")
    SSL_KEY_FILE: str = os.getenv("SSL_KEY_FILE", "certs/key.pem")
    SSL_CA_CERTS: str = os.getenv("SSL_CA_CERTS", "")  # Opcional, para certificados intermediários


settings = Settings()

