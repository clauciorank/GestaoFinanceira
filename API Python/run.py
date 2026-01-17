#!/usr/bin/env python3
"""
Script para executar a aplicação
"""
import uvicorn
import os
from app.config import settings

if __name__ == "__main__":
    # Configurações básicas
    config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": int(os.getenv("PORT", 8001)),
        "reload": os.getenv("RELOAD", "true").lower() == "true"
    }
    
    # Configurações SSL se HTTPS estiver habilitado
    if settings.USE_HTTPS:
        cert_file = settings.SSL_CERT_FILE
        key_file = settings.SSL_KEY_FILE
        
        # Verifica se os arquivos de certificado existem
        if not os.path.exists(cert_file):
            print(f"⚠️  Certificado SSL não encontrado: {cert_file}")
            print("💡 Execute: python scripts/generate_cert.py")
            print("   Ou configure USE_HTTPS=false no .env")
            exit(1)
        
        if not os.path.exists(key_file):
            print(f"⚠️  Chave SSL não encontrada: {key_file}")
            print("💡 Execute: python scripts/generate_cert.py")
            print("   Ou configure USE_HTTPS=false no .env")
            exit(1)
        
        config["ssl_certfile"] = cert_file
        config["ssl_keyfile"] = key_file
        
        if settings.SSL_CA_CERTS and os.path.exists(settings.SSL_CA_CERTS):
            config["ssl_ca_certs"] = settings.SSL_CA_CERTS
        
        print(f"🔒 HTTPS habilitado")
        print(f"   Certificado: {cert_file}")
        print(f"   Chave: {key_file}")
        print(f"   Acesse: https://localhost:{config['port']}")
        print(f"   ⚠️  IMPORTANTE: Use HTTPS (não HTTP) para acessar a aplicação")
    else:
        print(f"🌐 HTTP (sem SSL)")
        print(f"   Acesse: http://localhost:{config['port']}")
    
    uvicorn.run(**config)

