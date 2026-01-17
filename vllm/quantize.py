from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = "models/llm/qwen2.5-3b-instruct"
quant_path = "models/llm/qwen2.5-3b-instruct-awq"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoAWQForCausalLM.from_pretrained(
    model_path,
    device_map="cuda",
    safetensors=True
)

model.quantize(tokenizer, quant_config={
    "w_bit": 4,
    "q_group_size": 128,
    "zero_point": True
})

model.save_quantized(quant_path)
tokenizer.save_pretrained(quant_path)
