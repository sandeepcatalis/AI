import requests
from base import url, model



def single_query():
    """Run one simple query."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Summarize: Artificial intelligence is changing industries."}]
    }
    response = requests.post(url, json=payload).json()
    print("\n=== Single Query ===")
    print(response["choices"][0]["message"]["content"])


def batch_queries():
    """Run multiple prompts in sequence."""
    prompts = [
        "Summarize: Artificial intelligence is changing industries.",
        "Translate to Spanish: The weather is nice today.",
        "List three fruits in JSON format."
    ]

    print("\n=== Batch Queries ===")
    for i, p in enumerate(prompts, start=1):
        payload = {"model": model, "messages": [{"role": "user", "content": p}]}
        response = requests.post(url, json=payload).json()
        print(f"\n--- Query {i}: {p} ---")
        print(response["choices"][0]["message"]["content"])


def streaming_response():
    """Stream tokens as they are generated."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Write a short poem about AI in 3 lines."}],
        "stream": True
    }

    print("\n=== Streaming Response ===")
    with requests.post(url, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                if decoded.startswith("data: "):  # OpenAI style events
                    print(decoded.replace("data: ", ""), end="", flush=True)
    print("\n--- End of Stream ---")


def switch_model(new_model="mistral-7b-instruct"):
    """Swap to a different model loaded in LM Studio."""
    payload = {
        "model": new_model,
        "messages": [{"role": "user", "content": "Say hello from the new model."}]
    }
    response = requests.post(url, json=payload).json()
    print(f"\n=== Model Switch ({new_model}) ===")
    print(response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    print("Phase 3 – Running LLMs")
    print("1. Single Query")
    print("2. Batch Queries")
    print("3. Streaming Response")
    print("4. Switch Model")

    choice = input("\nChoose an option (1-4): ")

    if choice == "1":
        single_query()
    elif choice == "2":
        batch_queries()
    elif choice == "3":
        streaming_response()
    elif choice == "4":
        model_name = input("Enter model name (e.g., mistral-7b-instruct): ")
        switch_model(model_name)
    else:
        print("Invalid choice.")
