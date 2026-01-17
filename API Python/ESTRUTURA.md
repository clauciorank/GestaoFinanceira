# Estrutura do Projeto - Gestor Financeiro

## 📁 Organização dos Arquivos

```
API Python/
├── app/                          # Aplicação principal
│   ├── __init__.py
│   ├── main.py                   # Ponto de entrada (apenas inicialização)
│   ├── config.py                 # Configurações centralizadas
│   │
│   ├── core/                     # Núcleo da aplicação
│   │   ├── __init__.py
│   │   ├── app.py                # Criação e configuração do FastAPI
│   │   └── routes.py             # Rotas principais (/, /health)
│   │
│   ├── api/                      # Rotas da API REST
│   │   ├── __init__.py           # Agrupa todos os routers
│   │   ├── processamento.py      # Rotas de processamento (texto/áudio)
│   │   └── gastos.py             # Rotas CRUD de gastos
│   │
│   ├── models/                   # Modelos de dados
│   │   ├── __init__.py
│   │   └── schemas.py            # Modelos Pydantic (validação)
│   │
│   ├── services/                 # Serviços de negócio
│   │   ├── __init__.py
│   │   ├── transcription_service.py  # Serviço Whisper
│   │   └── llm_service.py            # Serviço LLM (LangChain)
│   │
│   └── database/                 # Banco de dados
│       ├── __init__.py
│       └── models.py             # Modelos ORM (SQLAlchemy)
│
├── templates/                    # Templates HTML
│   └── index.html                # Interface web
│
├── requirements.txt              # Dependências Python
├── .env.example                  # Exemplo de configuração
├── run.py                        # Script para executar
├── start.sh                      # Script bash de inicialização
└── exemplo_uso.py                # Exemplos de uso da API
```

## 🎯 Responsabilidades

### `app/main.py`
- **Responsabilidade**: Apenas inicialização da aplicação
- **Conteúdo**: Cria o app e inclui os routers

### `app/core/app.py`
- **Responsabilidade**: Configuração da aplicação FastAPI
- **Conteúdo**: 
  - Criação do app FastAPI
  - Configuração de CORS
  - Inicialização do banco de dados
  - Configuração de arquivos estáticos

### `app/core/routes.py`
- **Responsabilidade**: Rotas principais da aplicação
- **Rotas**:
  - `GET /` - Interface web
  - `GET /health` - Health check

### `app/api/processamento.py`
- **Responsabilidade**: Processamento de entrada (texto/áudio)
- **Rotas**:
  - `POST /api/processar-texto` - Processa texto
  - `POST /api/processar-audio` - Processa áudio

### `app/api/gastos.py`
- **Responsabilidade**: CRUD de gastos
- **Rotas**:
  - `GET /api/gastos` - Lista gastos
  - `GET /api/gastos/{id}` - Obtém um gasto
  - `POST /api/gastos` - Cria gasto manualmente
  - `DELETE /api/gastos/{id}` - Deleta um gasto

### `app/api/__init__.py`
- **Responsabilidade**: Agrupa todos os routers da API
- **Conteúdo**: Cria o `api_router` que inclui todos os routers

## 🔄 Fluxo de Requisição

1. **Requisição chega** → `app/main.py` (app FastAPI)
2. **Roteamento** → `app/core/routes.py` ou `app/api/__init__.py`
3. **Processamento** → `app/api/processamento.py` ou `app/api/gastos.py`
4. **Serviços** → `app/services/` (LLM, Transcrição)
5. **Banco de Dados** → `app/database/models.py`
6. **Resposta** → Modelos validados em `app/models/schemas.py`

## ✅ Vantagens da Nova Estrutura

1. **Separação de Responsabilidades**: Cada arquivo tem uma função clara
2. **Manutenibilidade**: Fácil encontrar e modificar código específico
3. **Escalabilidade**: Fácil adicionar novas rotas e funcionalidades
4. **Testabilidade**: Cada módulo pode ser testado independentemente
5. **Organização**: Estrutura clara e intuitiva

## 🚀 Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python run.py
# ou
./start.sh
```

