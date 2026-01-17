from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Qwen/Qwen2.5-3B-Instruct",
    local_dir="models/llm/qwen2.5-3b-instruct",
    local_dir_use_symlinks=False
)
