from llama_cpp import Llama

print("Loading model...")
llm = Llama(
    model_path="models/llm/llama.gguf",
    n_ctx=2048,
    n_threads=6,
    n_gpu_layers=0
)
print("Model loaded successfully!")
