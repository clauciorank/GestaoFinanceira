"""
Exemplos de uso da API
"""
import requests
import json

BASE_URL = "http://localhost:8001/api"

def exemplo_processar_texto():
    """Exemplo de processamento de texto"""
    print("📝 Processando texto...")
    response = requests.post(
        f"{BASE_URL}/processar-texto",
        json={"texto": "Gastei 50 reais com almoço hoje"}
    )
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def exemplo_processar_audio():
    """Exemplo de processamento de áudio"""
    print("🎤 Processando áudio...")
    with open("5109349681515726386.ogg", "rb") as f:
        files = {"file": ("audio.ogg", f, "audio/ogg")}
        response = requests.post(
            f"{BASE_URL}/processar-audio",
            files=files
        )
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def exemplo_listar_gastos():
    """Exemplo de listagem de gastos"""
    print("📊 Listando gastos...")
    response = requests.get(f"{BASE_URL}/gastos")
    print(f"Status: {response.status_code}")
    gastos = response.json()
    print(f"Total de gastos: {len(gastos)}")
    for gasto in gastos:
        print(f"  - {gasto['item']}: R$ {gasto['valor']:.2f} ({gasto['categoria']})")
    print()


def exemplo_criar_gasto_manual():
    """Exemplo de criação manual de gasto"""
    print("➕ Criando gasto manualmente...")
    response = requests.post(
        f"{BASE_URL}/gastos",
        json={
            "valor": 25.50,
            "item": "Café da manhã",
            "categoria": "Alimentação",
            "descricao_original": "Café da manhã no restaurante"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("EXEMPLOS DE USO DA API - GESTOR FINANCEIRO")
    print("=" * 50)
    print()
    
    try:
        # Verifica se a API está rodando
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            print("✅ API está rodando!")
            print()
        else:
            print("⚠️  API retornou status diferente de 200")
    except requests.exceptions.ConnectionError:
        print("❌ Erro: API não está rodando. Execute 'python run.py' primeiro.")
        exit(1)
    
    # Executa exemplos
    exemplo_processar_texto()
    exemplo_listar_gastos()
    exemplo_criar_gasto_manual()
    exemplo_listar_gastos()
    
    # Descomente para testar áudio (requer arquivo de áudio)
    # exemplo_processar_audio()

