from faster_whisper import WhisperModel
import os

MODEL_NAME = "small"
# Garante que o caminho seja absoluto e limpo
CACHE_DIR = os.path.abspath("./whisper_models")

# Configura as variáveis de ambiente para o local desejado
os.environ["HF_HOME"] = CACHE_DIR
os.environ["TRANSFORMERS_CACHE"] = CACHE_DIR

print(f"🔍 Verificando modelo Whisper '{MODEL_NAME}'...")

try:
    # 1. Tenta carregar apenas arquivos locais primeiro
    model = WhisperModel(
        MODEL_NAME,
        device="cpu",
        compute_type="int8",
        download_root=CACHE_DIR,
        local_files_only=True  # Não tenta baixar nada
    )
    print(f"✅ Modelo carregado do cache local: {CACHE_DIR}")

except (OSError, ValueError, Exception):
    # 2. Se falhar (modelo não existe), ele faz o download
    print(f"📥 Modelo não encontrado. Iniciando download em {CACHE_DIR}...")
    model = WhisperModel(
        MODEL_NAME,
        device="cpu",
        compute_type="int8",
        download_root=CACHE_DIR,
        local_files_only=False  # Permite o download
    )
    print("✅ Download e carregamento concluídos!")
