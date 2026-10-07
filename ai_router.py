from ollama import chat
import re

# ----------------------------
# Complexity Detection
# ----------------------------

COMPLEX_KEYWORDS = [
    "explain",
    "why",
    "how",
    "write",
    "code",
    "python",
    "program",
    "algorithm",
    "essay",
    "project",
    "compare",
    "difference",
    "math",
    "physics",
    "chemistry",
    "calculate",
    "design",
    "create",
]

MATH_SYMBOLS = re.compile(r"[\+\-\*/=<>^]")


def is_complex(prompt: str) -> bool:
    """
    Returns True if the prompt should go to the larger model.
    """

    prompt = prompt.lower()

    score = 0

    if len(prompt.split()) > 15:
        score += 1

    for word in COMPLEX_KEYWORDS:
        if word in prompt:
            score += 2

    if MATH_SYMBOLS.search(prompt):
        score += 1

    return score >= 3


# ----------------------------
# Ollama Chat
# ----------------------------

def ask(prompt: str):
    """
    Routes the prompt to the appropriate model.
    """

    if is_complex(prompt):
        model = "jarvis"
    else:
        model = "jarvis-llama-real"

    print(f"[AI Router] Selected model: {model}")

    try:
        response = chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "model": model,
            "response": response["message"]["content"]
        }

    except Exception as e:
        return f"[AI ERROR] {e}"


# ----------------------------
# Test
# ----------------------------

if __name__ == "__main__":

    while True:

        q = input(">>> ")

        if q.lower() in ("exit", "quit"):
            break

        print()
        print(ask(q))
        print()