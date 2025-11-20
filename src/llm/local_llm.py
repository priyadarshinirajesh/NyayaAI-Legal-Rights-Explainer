from llama_cpp import Llama

class LocalLLM:
    def __init__(self, model_path="models/llm/llama.gguf"):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=6,
            n_gpu_layers=0
        )

    def generate(self, prompt, max_tokens=300):
        result = self.llm(
            prompt,
            max_tokens=max_tokens,
            stop=["User:", "Assistant:"]
        )
        return result["choices"][0]["text"].strip()

