# Gestor Financeiro - Backend API

Backend para aplicação de gestão financeira que recebe texto ou áudio e salva informações estruturadas em banco de dados.

## 🚀 Funcionalidades

- ✅ Processamento de texto para extração de dados financeiros
- ✅ Processamento de áudio (transcrição + extração)
- ✅ Armazenamento estruturado em banco de dados
- ✅ Interface web moderna e responsiva
- ✅ API REST completa
- ✅ Suporte para modelos locais (Whisper + LLM via vLLM)
- ✅ Fácil migração para APIs originais (OpenAI, etc.)

## 📁 Estrutura do Projeto

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── config.py            # Configurações centralizadas
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # Rotas da API
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Modelos Pydantic
│   ├── services/
│   │   ├── __init__.py
│   │   ├── transcription_service.py  # Serviço Whisper
│   │   └── llm_service.py            # Serviço LLM
│   └── database/
│       ├── __init__.py
│       └── models.py        # Modelos ORM e configuração do banco
├── templates/
│   └── index.html           # Interface web
├── static/                  # Arquivos estáticos (opcional)
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ Instalação

1. **Clone o repositório e instale as dependências:**

```bash
pip install -r requirements.txt
```

2. **Configure as variáveis de ambiente:**

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Whisper (local)
WHISPER_MODE=local
WHISPER_URL_LOCAL=http://localhost:8000/transcribe

# LLM (local via vLLM)
LLM_MODE=local
LLM_URL_LOCAL=http://localhost:8002/v1
LLM_MODEL_LOCAL=neuralmagic/Llama-3.2-3B-Instruct-quantized.w8a8
LLM_API_KEY=EMPTY

# Banco de dados
DATABASE_URL=sqlite:///./gestor_financeiro.db
```

3. **Certifique-se de que os serviços estão rodando:**

- **Whisper**: `http://localhost:8000/transcribe`
- **vLLM**: `http://localhost:8002/v1`

## 🚀 Executando a Aplicação

```bash
# Opção 1: Script Python (recomendado)
python run.py

# Opção 2: Usando uvicorn diretamente
uvicorn app.main:app --reload --port 8001

# Opção 3: Executando o main.py
python -m app.main
```

A aplicação estará disponível em:
- **API**: http://localhost:8001 (ou https://localhost:8001 se HTTPS estiver habilitado)
- **Interface Web**: http://localhost:8001
- **Documentação**: http://localhost:8001/docs

### 🔒 HTTPS (Conexão Segura)

Para habilitar HTTPS, consulte o arquivo [HTTPS.md](HTTPS.md) para instruções detalhadas.

**Resumo rápido:**
```bash
# 1. Gerar certificados (desenvolvimento)
python scripts/generate_cert.py

# 2. Configurar .env
USE_HTTPS=true

# 3. Executar
python run.py
```

## 📡 Endpoints da API

### Processar Texto
```http
POST /api/processar-texto
Content-Type: application/json

{
  "texto": "Gastei 50 reais com almoço hoje"
}
```

### Processar Áudio
```http
POST /api/processar-audio
Content-Type: multipart/form-data

file: [arquivo de áudio]
```

### Listar Gastos
```http
GET /api/gastos?skip=0&limit=100
```

### Obter Gasto
```http
GET /api/gastos/{id}
```

### Criar Gasto Manualmente
```http
POST /api/gastos
Content-Type: application/json

{
  "valor": 50.0,
  "item": "Almoço",
  "categoria": "Alimentação",
  "descricao_original": "Gastei 50 reais com almoço"
}
```

### Deletar Gasto
```http
DELETE /api/gastos/{id}
```

## 🔄 Migrando para APIs Originais

Para usar APIs originais (OpenAI, etc.), edite o arquivo `.env`:

```env
# Whisper (API original)
WHISPER_MODE=api
WHISPER_URL_API=https://api.openai.com/v1/audio/transcriptions

# LLM (OpenAI)
LLM_MODE=api
LLM_URL_API=https://api.openai.com/v1
LLM_API_KEY=sk-...
```

E atualize os serviços em `app/services/` conforme necessário.

## 🗄️ Banco de Dados

Por padrão, a aplicação usa SQLite. Para usar PostgreSQL ou MySQL:

1. Instale o driver apropriado:
   - PostgreSQL: `pip install psycopg2-binary`
   - MySQL: `pip install pymysql`

2. Atualize `DATABASE_URL` no `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

## 🎨 Interface Web

A interface web está disponível em `http://localhost:8001` e oferece:

- 📝 **Aba Texto**: Digite ou cole texto para processar
- 🎤 **Aba Áudio**: Envie arquivo de áudio para transcrição e processamento
- 📊 **Aba Gastos**: Visualize todos os gastos registrados

## 📝 Categorias Suportadas

- Alimentação
- Transporte
- Lazer
- Saúde
- Moradia
- Outros

## 🔧 Desenvolvimento

Para desenvolvimento com hot-reload:

```bash
uvicorn app.main:app --reload --port 8001
```

## 🔒 Segurança

- **HTTPS**: Configure HTTPS para produção. Veja [HTTPS.md](HTTPS.md) para detalhes.
- **Variáveis de Ambiente**: Nunca commite arquivos `.env` com informações sensíveis.
- **Certificados**: Use certificados de CA confiável em produção (Let's Encrypt, etc.).

## 📄 Licença

Este projeto é de uso pessoal.

