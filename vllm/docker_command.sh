docker run --gpus all \
    -v huggingface:/root/.cache/huggingface \
    -p 8002:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model neuralmagic/Llama-3.2-3B-Instruct-quantized.w8a8 \
    --gpu-memory-utilization 0.7 \
    --max-model-len 8192
