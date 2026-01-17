"""
Rotas de processamento de texto e áudio
"""
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database.models import get_db, Gasto
from app.models.schemas import ProcessamentoRequest, ProcessamentoResponse, GastoResponse
from app.services.transcription_service import TranscriptionService
from app.services.llm_service import LLMService

router = APIRouter()

# Inicializa serviços
transcription_service = TranscriptionService()
llm_service = LLMService()


@router.post("/processar-texto", response_model=ProcessamentoResponse)
async def processar_texto(
    request: ProcessamentoRequest,
    db: Session = Depends(get_db)
):
    """
    Processa um texto e extrai dados financeiros, salvando no banco de dados
    """
    try:
        # Processa o texto com LLM
        resultado = llm_service.processar(request.texto)
        
        if "erro" in resultado:
            return ProcessamentoResponse(
                sucesso=False,
                erro=resultado["erro"],
                texto_processado=request.texto
            )
        
        # Cria o gasto no banco de dados
        gasto_db = Gasto(
            valor=resultado["valor"],
            item=resultado["item"],
            categoria=resultado["categoria"],
            meio_pagamento=resultado.get("meio_pagamento"),
            descricao_original=request.texto
        )
        
        db.add(gasto_db)
        db.commit()
        db.refresh(gasto_db)
        
        gasto_response = GastoResponse(
            id=gasto_db.id,
            valor=gasto_db.valor,
            item=gasto_db.item,
            categoria=gasto_db.categoria,
            meio_pagamento=gasto_db.meio_pagamento,
            descricao_original=gasto_db.descricao_original,
            data_criacao=gasto_db.data_criacao
        )
        
        return ProcessamentoResponse(
            sucesso=True,
            gasto=gasto_response,
            texto_processado=request.texto
        )
        
    except Exception as e:
        db.rollback()
        return ProcessamentoResponse(
            sucesso=False,
            erro=f"erro_interno: {str(e)}",
            texto_processado=request.texto
        )


@router.post("/processar-audio", response_model=ProcessamentoResponse)
async def processar_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Processa um arquivo de áudio, transcreve e extrai dados financeiros
    """
    try:
        # Lê o conteúdo do arquivo
        file_content = await file.read()
        
        # Detecta o tipo MIME se não fornecido
        content_type = file.content_type
        if not content_type:
            filename = file.filename or "audio.webm"
            if filename.endswith(".webm"):
                content_type = "audio/webm"
            elif filename.endswith(".mp3"):
                content_type = "audio/mpeg"
            elif filename.endswith(".wav"):
                content_type = "audio/wav"
            elif filename.endswith(".m4a"):
                content_type = "audio/mp4"
            else:
                content_type = "audio/webm"  # Padrão para gravações do navegador
        
        # Transcreve o áudio
        texto_transcrito = transcription_service.transcrever(
            file_content=file_content,
            filename=file.filename or "gravacao.webm",
            content_type=content_type
        )
        
        if not texto_transcrito or not texto_transcrito.strip():
            return ProcessamentoResponse(
                sucesso=False,
                erro="transcricao_vazia",
                texto_processado=""
            )
        
        # Processa o texto transcrito com LLM
        resultado = llm_service.processar(texto_transcrito)
        
        if "erro" in resultado:
            return ProcessamentoResponse(
                sucesso=False,
                erro=resultado["erro"],
                texto_processado=texto_transcrito
            )
        
        # Cria o gasto no banco de dados
        gasto_db = Gasto(
            valor=resultado["valor"],
            item=resultado["item"],
            categoria=resultado["categoria"],
            meio_pagamento=resultado.get("meio_pagamento"),
            descricao_original=texto_transcrito
        )
        
        db.add(gasto_db)
        db.commit()
        db.refresh(gasto_db)
        
        gasto_response = GastoResponse(
            id=gasto_db.id,
            valor=gasto_db.valor,
            item=gasto_db.item,
            categoria=gasto_db.categoria,
            meio_pagamento=gasto_db.meio_pagamento,
            descricao_original=gasto_db.descricao_original,
            data_criacao=gasto_db.data_criacao
        )
        
        return ProcessamentoResponse(
            sucesso=True,
            gasto=gasto_response,
            texto_processado=texto_transcrito
        )
        
    except Exception as e:
        db.rollback()
        return ProcessamentoResponse(
            sucesso=False,
            erro=f"erro_interno: {str(e)}",
            texto_processado=""
        )

