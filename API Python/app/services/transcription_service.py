"""
Serviço de transcrição de áudio usando Whisper
Suporta modo local e API original
"""
import os
import requests
from fastapi import HTTPException
from app.config import settings


class TranscriptionService:
    """Serviço para transcrever áudio em texto"""
    
    def __init__(self):
        self.mode = settings.WHISPER_MODE
        self.url = settings.WHISPER_URL
    
    def transcrever(self, file_content: bytes, filename: str, content_type: str) -> str:
        """
        Transcreve arquivo de áudio em texto
        
        Args:
            file_content: Conteúdo do arquivo em bytes
            filename: Nome do arquivo
            content_type: Tipo MIME do arquivo
            
        Returns:
            Texto transcrito
            
        Raises:
            HTTPException: Se houver erro na transcrição
        """
        url = self.url
        
        try:
            files = {
                'file': (filename, file_content, content_type)
            }
            response = requests.post(url, files=files, timeout=60)
            response.raise_for_status()
            
            resultado = response.json()
            return resultado.get("text", "")
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na conexão com serviço de transcrição: {e}"
            print(error_msg)
            raise HTTPException(
                status_code=502,
                detail=f"Serviço de transcrição indisponível: {str(e)}"
            )
        except Exception as e:
            error_msg = f"Erro ao processar transcrição: {e}"
            print(error_msg)
            raise HTTPException(
                status_code=500,
                detail=error_msg
            )
    
    def transcrever_arquivo_local(self, file_path: str) -> str:
        """
        Transcreve um arquivo de áudio do disco local
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Texto transcrito
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        with open(file_path, "rb") as arquivo:
            conteudo = arquivo.read()
            filename = os.path.basename(file_path)
            
            # Detecta o tipo MIME baseado na extensão
            content_type = "audio/ogg"
            if filename.endswith(".mp3"):
                content_type = "audio/mpeg"
            elif filename.endswith(".wav"):
                content_type = "audio/wav"
            elif filename.endswith(".m4a"):
                content_type = "audio/mp4"
            elif filename.endswith(".webm"):
                content_type = "audio/webm"
            elif filename.endswith(".ogg"):
                content_type = "audio/ogg"
            
            return self.transcrever(conteudo, filename, content_type)

