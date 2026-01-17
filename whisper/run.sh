docker run --gpus all \
  --name whisper-api \
  -p 8000:8000 \
  -v $(pwd)/whisper_models:/models \
  -e HF_HOME=/models \
  -e TRANSFORMERS_CACHE=/models \
  whisper-api
