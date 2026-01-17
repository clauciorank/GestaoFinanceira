FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Instalando dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalando bibliotecas NVIDIA via pip (essencial para o Faster Whisper no CUDA 12)
RUN pip3 install --no-cache-dir \
    nvidia-cublas-cu12 \
    nvidia-cudnn-cu12

# Configurando o caminho das bibliotecas para o Python 3.10 (Ubuntu 22.04)
ENV LD_LIBRARY_PATH="/usr/local/lib/python3.10/dist-packages/nvidia/cudnn/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cublas/lib:$LD_LIBRARY_PATH"

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
