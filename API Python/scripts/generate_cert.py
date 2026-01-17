#!/usr/bin/env python3
"""
Script para gerar certificados SSL auto-assinados para desenvolvimento
"""
import os
import subprocess
from pathlib import Path

def generate_self_signed_cert():
    """Gera certificado SSL auto-assinado para desenvolvimento"""
    
    # Cria o diretório de certificados se não existir
    certs_dir = Path("certs")
    certs_dir.mkdir(exist_ok=True)
    
    cert_file = certs_dir / "cert.pem"
    key_file = certs_dir / "key.pem"
    
    # Verifica se já existem certificados
    if cert_file.exists() and key_file.exists():
        print("⚠️  Certificados já existem!")
        resposta = input("Deseja regenerar? (s/N): ")
        if resposta.lower() != 's':
            print("Operação cancelada.")
            return
    
    print("🔐 Gerando certificado SSL auto-assinado...")
    print("   (Apenas para desenvolvimento - não use em produção!)")
    print()
    
    # Comando openssl para gerar certificado auto-assinado
    cmd = [
        "openssl", "req", "-x509", "-newkey", "rsa:4096",
        "-nodes", "-out", str(cert_file),
        "-keyout", str(key_file),
        "-days", "365",
        "-subj", "/C=BR/ST=State/L=City/O=GestorFinanceiro/CN=localhost"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("✅ Certificados gerados com sucesso!")
        print(f"   Certificado: {cert_file}")
        print(f"   Chave: {key_file}")
        print()
        print("⚠️  IMPORTANTE:")
        print("   - Estes são certificados auto-assinados (apenas para desenvolvimento)")
        print("   - Seu navegador mostrará um aviso de segurança (isso é normal)")
        print("   - Para produção, use certificados de uma CA confiável (Let's Encrypt, etc.)")
        print()
        print("💡 Para usar HTTPS, configure no .env:")
        print("   USE_HTTPS=true")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao gerar certificados: {e}")
        print()
        print("💡 Certifique-se de que o OpenSSL está instalado:")
        print("   Ubuntu/Debian: sudo apt-get install openssl")
        print("   macOS: brew install openssl")
        print("   Windows: Baixe de https://slproweb.com/products/Win32OpenSSL.html")
    except FileNotFoundError:
        print("❌ OpenSSL não encontrado!")
        print()
        print("💡 Instale o OpenSSL:")
        print("   Ubuntu/Debian: sudo apt-get install openssl")
        print("   macOS: brew install openssl")
        print("   Windows: Baixe de https://slproweb.com/products/Win32OpenSSL.html")

if __name__ == "__main__":
    generate_self_signed_cert()

