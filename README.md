# 💰 Gestor Financeiro Inteligente

Um sistema completo de gestão financeira pessoal que utiliza Inteligência Artificial para processar gastos via texto e áudio. O projeto integra reconhecimento de fala (Whisper), processamento de linguagem natural (LLM) e dashboards interativos.

## 🏗️ Arquitetura do Projeto

O sistema é composto por microsserviços containerizados via Docker:

*   **API Python (FastAPI)**: Núcleo do sistema. Gerencia regras de negócio, processa entradas e expõe a interface web.
*   **Whisper Service**: Microsserviço dedicado para transcrição de áudio de alta performance (suporte a GPU).
*   **MySQL**: Banco de dados relacional robusto para persistência dos dados.
*   **Metabase**: Ferramenta de Business Intelligence para visualização avançada e insights dos seus gastos.

## 🚀 Como Usar

### Pré-requisitos

*   [Docker](https://www.docker.com/) e Docker Compose instalados.
*   (Opcional) Drivers NVIDIA configurados para aceleração de GPU no Whisper.

### Instalação Rápida

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/clauciorank/GestaoFinanceira.git
    cd GestaoFinanceira
    ```

2.  **Configure o ambiente:**
    Copie o exemplo de configuração:
    ```bash
    cp .env.example .env
    ```
    *Edite o arquivo `.env` se desejar alterar senhas ou chaves de API, mas os padrões funcionam para teste local.*

3.  **Inicie a aplicação:**
    Utilize o script de automação que verifica dependências, baixa modelos de IA necessários e sobe os containers:
    ```bash
    ./run_apps.sh
    ```

### 🌐 Acessando os Serviços

Após iniciar, os serviços estarão disponíveis em:

| Serviço | URL | Descrição |
| :--- | :--- | :--- |
| **Aplicação Web / API** | [http://localhost:8000](http://localhost:8000) | Interface principal para lançar gastos e API Swagger. |
| **Metabase (Dashboards)** | [http://localhost:3000](http://localhost:3000) | Crie gráficos e visualize seus dados. |

> **Nota:** A API roda internamente na porta 8001, mas é exposta na 8000 pelo Docker Compose.

## 🛠️ Desenvolvimento e Manutenção

*   **Modelos de IA**: Os modelos do Whisper são baixados automaticamente para a pasta `whisper_models/` na primeira execução.
*   **Banco de Dados**: O MySQL armazena os dados no volume Docker `db_data`.
*   **API Backend**: Para detalhes de desenvolvimento do backend, consulte [API Python/README.md](API%20Python/README.md).

## 🔒 Segurança

*   O arquivo `.env` contém segredos e **não** é versionado no Git.
*   O arquivo `run_apps.sh` facilita o setup seguro garantindo que modelos e dependências estejam presentes.
