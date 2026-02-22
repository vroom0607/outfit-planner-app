import os
from threading import Lock

# Must be set before importing llama_cpp so backend initialization sees it.
os.environ.setdefault("GGML_USE_METAL", "0")
os.environ.setdefault("LLAMA_METAL", "0")

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

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


def _fallback_explanation(outfit, weather, event_type):
    outfit_items = [i.name for i in outfit if getattr(i, "name", None)]
    pieces = ", ".join(outfit_items) if outfit_items else "this outfit"
    return (
        f"This look works well for {event_type}. "
        f"{pieces} balances comfort and style for around {weather['temp']}°F with "
        f"{weather['precipitation']} inches of precipitation expected."
    )


def get_model():
    global llm
    if llm is None:
        with llm_lock:
            if llm is None:
                if Llama is None:
                    print("llama_cpp is not installed. Falling back to template explanation.")
                    llm = False
                    return llm
                try:
                    llm = Llama(
                        model_path="models/Llama-3.2-3B-Instruct-Q4_0.gguf",
                        n_ctx=_env_int("LLM_N_CTX", 512),
                        n_threads=_env_int("LLM_N_THREADS", 2),
                        n_batch=_env_int("LLM_N_BATCH", 32),
                        n_gpu_layers=0,
                        use_mmap=True,
                        use_mlock=False,
                        verbose=True,
                    )
                except Exception as exc:
                    print(f"Failed to initialize Llama model. Falling back to template explanation: {exc}")
                    llm = False
    return llm


def generate_explanation(outfit, weather, event_type):
    llm_instance = get_model()
    if not llm_instance:
        yield _fallback_explanation(outfit, weather, event_type)
        return

    outfit_items = [{"name": i.name, "category": i.category} for i in outfit]
    item_descriptions = ", ".join(
        [f"{item['name']} ({item['category']})" for item in outfit_items]
    )

    prompt = (
        f"You are a helpful fashion assistant. Explain why this outfit works in 4 sentences. Mention the temperature, preciptiation, and event, and only talk about clothing given to you: "
        f"{item_descriptions}. Weather: {weather['temp']}°F, {weather['precipitation']} inches of precipitation. "
        f"Event: {event_type}."
    )

    templated_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"

    llm_instance.reset()

    try:
        response_iter = llm_instance.create_completion(
            prompt=templated_prompt,
            max_tokens=200,
            temperature=0.4,
            stream=True,
        )
        for chunk in response_iter:
            delta = chunk.get("choices", [{}])[0].get("text", "")
            if delta:
                yield delta
    except Exception as exc:
        print(f"Streaming completion failed, returning template explanation: {exc}")
        yield _fallback_explanation(outfit, weather, event_type)
