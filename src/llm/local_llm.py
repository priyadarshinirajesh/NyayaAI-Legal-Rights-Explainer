# src/llm/local_llm.py
from llama_cpp import Llama

class LocalLLM:
    def __init__(self):
        self.llm = Llama(
            model_path="models/llm/llama.gguf",
            n_ctx=8192,
            n_threads=8,
            n_gpu_layers=0,
            verbose=False
        )

    def generate(self, prompt, max_tokens=500):
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.2,
            top_p=0.9,
        )
        return response["choices"][0]["text"]
