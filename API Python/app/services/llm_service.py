"""
Serviço de processamento de texto usando LLM
Suporta modo local (vLLM) e APIs originais (OpenAI, etc.)
"""
from typing import Optional, Dict, Any
import json
import re
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings
from app.models.schemas import GastoFinanceiro


class LLMService:
    """Serviço para processar texto e extrair dados financeiros usando LLM"""
    
    def __init__(self):
        self.mode = settings.LLM_MODE
        self.llm = self._get_llm_connector()
        self.prompt_template = self._create_prompt_template()
    
    def _get_llm_connector(self):
        """Obtém o conector LLM baseado na configuração"""
        if self.mode == "local":
            return ChatOpenAI(
                model=settings.LLM_MODEL,
                openai_api_key=settings.LLM_API_KEY,
                openai_api_base=settings.LLM_URL,
                temperature=0,
                convert_system_message_to_human=True
            )
        elif self.mode == 'gemini':
            # Usando a biblioteca oficial do Google
            return ChatGoogleGenerativeAI(
                model="gemini-3-flash-preview",
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0,
                convert_system_message_to_human=True
            )
        else:
            # Para uso futuro com APIs originais (OpenAI, Anthropic, etc.)
            # Exemplo para OpenAI:
            # return ChatOpenAI(
            #     model="gpt-4",
            #     openai_api_key=settings.LLM_API_KEY,
            #     temperature=0
            # )
            raise ValueError(f"Modo LLM '{self.mode}' não implementado ainda")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Cria o template de prompt para extração de dados financeiros"""
        return ChatPromptTemplate.from_messages([
            ("system", """
            Você é um assistente especializado em contabilidade pessoal.

            REGRAS DE EXTRAÇÃO:
            1. Extraia apenas dados de gastos/despesas.
            2. Se a entrada for irrelevante, ofensiva ou não for um gasto, responda APENAS com: {{"erro": "nao_e_gasto"}}
            3. Se for um gasto, responda APENAS com um JSON válido no formato: {{"valor": float, "item": string, "categoria": string, "meio_pagamento": string (opcional)}}
            4. Não invente categorias. Use apenas: Alimentação, Transporte, Lazer, Saúde, Moradia, Outros, Bebida.
            5. Converta valores escritos por extenso (ex: "vinte reais") para números (20.0).
            6. Se o valor não estiver explícito, use 0.0 e marque como erro.
            7. Identifique o meio de pagamento se mencionado. Use APENAS: Crédito, Débito, Refeição, Pix. Se não identificar ou for diferente, use null.
            8. Responda APENAS com JSON, sem texto adicional.
            """),
            ("user", "{entrada}")
        ])
    
    def processar(self, texto: str) -> Dict[str, Any]:
        """
        Processa texto e extrai dados financeiros
        
        Args:
            texto: Texto a ser processado
            
        Returns:
            Dicionário com dados extraídos ou erro
        """
        if not texto or not texto.strip():
            return {"erro": "texto_vazio"}
        
        try:
            chain = self.prompt_template | self.llm
            
            resposta = chain.invoke({
                "entrada": texto.strip()
            })
            
            # Extrai o conteúdo da resposta
            resposta_texto = resposta.content.strip()
            
            # Remove markdown code blocks se existirem
            if "```json" in resposta_texto:
                resposta_texto = resposta_texto.split("```json")[1].split("```")[0].strip()
            elif "```" in resposta_texto:
                resposta_texto = resposta_texto.split("```")[1].split("```")[0].strip()
            
            # Tenta parsear como JSON
            try:
                dados = json.loads(resposta_texto)
            except json.JSONDecodeError:
                # Se não for JSON válido, tenta extrair JSON do texto
                json_match = re.search(r'\{[^}]+\}', resposta_texto)
                if json_match:
                    dados = json.loads(json_match.group())
                else:
                    return {"erro": "resposta_invalida"}
            
            # Verifica se há erro na resposta
            if "erro" in dados:
                return {"erro": dados.get("erro", "nao_e_gasto")}
            
            # Valida e cria o objeto Pydantic
            gasto = GastoFinanceiro(**dados)
            
            return {
                "valor": gasto.valor,
                "item": gasto.item,
                "categoria": gasto.categoria,
                "meio_pagamento": getattr(gasto, "meio_pagamento", None)
            }
            
        except ValueError as e:
            # Erro de validação do Pydantic (ex: valor negativo, formato inválido)
            error_msg = str(e)
            if "nao_e_gasto" in error_msg.lower() or "erro" in error_msg.lower():
                return {"erro": "nao_e_gasto"}
            return {"erro": f"dados_invalidos: {error_msg}"}
        except Exception as e:
            # Outros erros (erro de conexão, formato inválido, etc.)
            error_msg = str(e)
            print(f"Erro ao processar LLM: {error_msg}")
            # Verifica se é um erro de conexão
            if "connection" in error_msg.lower() or "timeout" in error_msg.lower():
                return {"erro": "servico_indisponivel"}
            return {"erro": f"falha_processamento: {error_msg}"}

