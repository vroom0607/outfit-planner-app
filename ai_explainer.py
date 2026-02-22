import os
from llama_cpp import Llama
from threading import Lock

# prevent Metal from being used
os.environ["GGML_USE_METAL"] = "0"

llm = None
llm_lock = Lock()

def get_model():
    global llm
    if llm is None:
        with llm_lock:
            if llm is None:
                llm = Llama(
                    model_path="models/llama-nano-tiny-cpu-fast-top-q4_k_m.gguf",
                    n_ctx=128,
                    n_threads=4,
                    n_gpu_layers=-1,
                    verbose=True
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

    response_iter = llm_instance.stream_complete(prompt=templated_prompt, max_tokens=100)
    for chunk in response_iter:
        yield chunk.delta.encode("utf-8")