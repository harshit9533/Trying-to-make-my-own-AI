from ollama import chat

def ask_model(prompt, model="jarvis"):
    response = chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]