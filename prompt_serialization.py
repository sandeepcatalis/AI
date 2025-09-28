from base import url, model
import requests


def chatml_example():
    """Prompt using ChatML format (used by OpenAI)."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Translate to French: Hello"}
        ]
    }
    response = requests.post(url, json=payload)
    print("\n=== ChatML Example ===")
    print(response.json()["choices"][0]["message"]["content"])


def alpaca_example():
    """Prompt using Alpaca format (used by LLaMA/Alpaca models)."""
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "### Instruction:\nTranslate to French: Hello\n\n### Response:"}
        ]
    }
    response = requests.post(url, json=payload)
    print("\n=== Alpaca Example ===")
    print(response.json()["choices"][0]["message"]["content"])


def inst_example():
    """Prompt using INST format (used by LLaMA-2)."""
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "[INST] <<SYS>>\nYou are a helpful assistant.\n<</SYS>>\n\nTranslate to French: Hello [/INST]"}
        ]
    }
    response = requests.post(url, json=payload)
    print("\n=== INST Example ===")
    print(response.json()["choices"][0]["message"]["content"])


if __name__ == "__main__":
    chatml_example()
    alpaca_example()
    inst_example()
if __name__ == "__main__":
    print("Choose an option:")
    print("1. ChatML Example")
    print("2. Alpaca Example")
    print("3. INST Example")

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        chatml_example()
    elif choice == "2":
        alpaca_example()
    elif choice == "3":
        inst_example()
    else:
        print("Invalid choice. Please try again.")