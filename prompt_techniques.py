import requests
import json
from base import url, model

# Function: Summarize Text
# Prompt Approach: Direct Instruction
# This function uses a direct instruction prompt to summarize a given text in one sentence.
def summarize_text():
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Summarize this text in one sentence: Artificial intelligence is transforming industries."}
        ]
    }

    response = requests.post(url, json=payload)
    print(response.json())

# Function: Translate to English
# Prompt Approach: One-Shot Prompting
# This function uses a one-shot example to demonstrate how to translate sentences from French to English.
def translate_to_english():
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": """Translate the following sentences to English.

                Example:
                French: Bonjour
                English: Good morning

                Now translate:
                French:Comment vas-tu?
                English:""",
            }
        ],
    }

    response = requests.post(url, json=payload)
    print(response.json()["choices"][0]["message"]["content"])

# Function: Solve Step by Step
# Prompt Approach: Chain-of-Thought Prompting
# This function uses chain-of-thought prompting to encourage the model to reason step by step.
def solve_step_by_step():
    payload = {
        "model": model,
        "messages": [
            {"role": "user",
             "content": "Let's solve step by step and show reasoning: If a train travels 60 km in 1 hour, how long will it take to travel 150 km?"}
        ],
        "stream": True
    }

    headers = {"Accept": "text/event-stream"}  # optional but nice

    final_text = []

    with requests.post(url, json=payload, headers=headers, stream=True) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            # Strip SSE prefix
            if line.startswith("data: "):
                line = line[6:]
            if line == "[DONE]":
                break

            try:
                chunk = json.loads(line)
            except json.JSONDecodeError:
                # not a JSON chunk, ignore/print for debug
                continue

            choice = chunk.get("choices", [{}])[0]
            delta = choice.get("delta", {})

            # live token-by-token print
            if "content" in delta:
                token = delta["content"]
                print(token, end="", flush=True)
                final_text.append(token)

    print("\n---\nFINAL:", "".join(final_text))

# Function: Classify Animals
# Prompt Approach: Few-Shot Prompting
# This function uses few-shot prompting by providing multiple examples to classify animals into categories.
def classify_animals():
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": """Classify each animal as Mammal, Bird, or Reptile.

Example:
Animal: Dog → Mammal
Animal: Eagle → Bird
Animal: Snake → Reptile

Now classify:
Animal: Dolphin →
Animal: Parrot →
Animal: Crocodile →""",
            }
        ],
    }

    response = requests.post(url, json=payload)
    print(response.json()["choices"][0]["message"]["content"])

# Function: Extract Details
# Prompt Approach: Structured Output Prompting
# This function uses structured output prompting to extract specific details from a text and return them in JSON format.
def extract_details():
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": """Extract details and return in JSON format:
"Shir was founded by Alex Kim in 2010 in Berlin."

Output JSON (example for Apple):
{
  \"company\": \"Apple\",
  \"founder\": \"Steve Jobs\",
  \"year\": 1976,
  \"location\": \"Cupertino\"
}"""
            }
        ]
    }

    response = requests.post(url, json=payload)
    print(response.json()["choices"][0]["message"]["content"])

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Summarize Text")
    print("2. Translate to English")
    print("3. Solve Step by Step")
    print("4. Classify Animals")
    print("5. Extract Details")

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        summarize_text()
    elif choice == "2":
        translate_to_english()
    elif choice == "3":
        solve_step_by_step()
    elif choice == "4":
        classify_animals()
    elif choice == "5":
        extract_details()
    else:
        print("Invalid choice. Please try again.")