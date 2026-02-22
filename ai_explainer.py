import os
from threading import Lock

from llama_cpp import Llama

# prevent Metal from being used
os.environ["GGML_USE_METAL"] = "0"

llm = None
llm_lock = Lock()


def _env_int(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default

def get_model():
    global llm
    if llm is None:
        with llm_lock:
            if llm is None:
                llm = Llama(
                    model_path="models/llama-nano-tiny-cpu-fast-top-q4_k_m.gguf",
                    n_ctx=_env_int("LLM_N_CTX", 96),
                    n_threads=_env_int("LLM_N_THREADS", 2),
                    n_batch=_env_int("LLM_N_BATCH", 32),
                    n_gpu_layers=0,
                    use_mmap=True,
                    use_mlock=False,
                    verbose=True,
                )
                print("Model loaded on device:", llm.device)
    return llm

def generate_explanation(outfit, weather, event_type):
    outfit_items = [{"name": i.name, "category": i.category} for i in outfit]
    item_descriptions = ", ".join(
        [f"{item['name']} ({item['category']})" for item in outfit_items]
    )

    prompt = (
        f"You are a helpful fashion assistant. Explain why this outfit works: "
        f"{item_descriptions}. Weather: {weather['temp']}°F, {weather['precipitation']} inches of precipitation. "
        f"Event: {event_type}."
    )

    templated_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"

    llm_instance = get_model()
    llm_instance.reset()

    response_iter = llm_instance.create_completion(
        prompt=templated_prompt,
        max_tokens=80,
        temperature=0.4,
        stream=True,
    )
    for chunk in response_iter:
        delta = chunk.get("choices", [{}])[0].get("text", "")
        if delta:
            yield delta
