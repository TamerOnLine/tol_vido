import requests
import re
import tiktoken
import os
from dotenv import load_dotenv


def load_model_name():
    """
    Load the model name from the active environment file specified in 'active_env.txt'.

    Returns:
        str: The model name retrieved from the environment file.

    Raises:
        RuntimeError: If MODEL_NAME is not found in the environment file.
    """
    with open("active_env.txt", "r", encoding="utf-8") as file:
        env_file = file.read().strip()

    load_dotenv(env_file)
    model_name = os.getenv("MODEL_NAME") or os.getenv("MODEL")

    if not model_name:
        raise RuntimeError("MODEL_NAME or MODEL not found in the .env file.")

    return model_name


API_URL = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = load_model_name()


def split_text_by_tokens(text, max_tokens=300):
    """
    Split the input text into smaller chunks based on token count.

    Args:
        text (str): The input text to split.
        max_tokens (int): Maximum number of tokens per chunk.

    Returns:
        list[str]: A list of text chunks not exceeding the specified token limit.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    sentences = re.split(r'(?<=[.؟!])\s+', text.strip())
    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = enc.encode(sentence)
        token_count = len(sentence_tokens)

        if token_count > max_tokens:
            for i in range(0, token_count, max_tokens):
                sub_tokens = sentence_tokens[i:i + max_tokens]
                sub_text = enc.decode(sub_tokens)
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                    current_tokens = 0
                chunks.append(sub_text.strip())
        elif current_tokens + token_count <= max_tokens:
            current_chunk += sentence + " "
            current_tokens += token_count
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
            current_tokens = token_count

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def format_text_to_paragraphs(raw_text: str) -> str:
    """
    Format raw text by adding proper punctuation using an LLM, without changing content.

    Args:
        raw_text (str): The unformatted raw text.

    Returns:
        str: The text with added punctuation, split into paragraphs.

    Raises:
        Exception: If the API call fails or returns an error.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    chunks = split_text_by_tokens(raw_text, max_tokens=300)
    formatted_chunks = []

    for chunk in chunks:
        response = requests.post(API_URL, json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Du bist ein Assistent, der nur Zeichensetzung "
                        "in einem deutschen Transkript ergänzt. "
                        "Du darfst absolut **nichts** am Textinhalt ändern. "
                        "Keine Umformulierungen, keine Löschungen, keine neuen Wörter oder Absätze."
                    )
                },
                {
                    "role": "user",
                    "content": "Bitte füge nur passende Zeichensetzung (.,!?…) zum folgenden Text hinzu. Verändere nichts."
                },
                {
                    "role": "user",
                    "content": chunk
                }
            ],
            "temperature": 0.0,
            "max_tokens": 1024
        })

        if response.status_code == 200:
            formatted = response.json()["choices"][0]["message"]["content"]
            formatted_chunks.append(formatted.strip())
        else:
            try:
                error_msg = response.json().get("error", {}).get("message", response.text)
            except Exception:
                error_msg = response.text
            raise Exception(f"LLM API Error {response.status_code}: {error_msg}")

    return "\n\n".join(formatted_chunks)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python format_text.py <input_file.txt>")
        sys.exit(1)

    input_path = sys.argv[1]
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print(f"File not found: {input_path}")
        sys.exit(1)

    formatted_text = format_text_to_paragraphs(raw_text)
    output_path = input_path.replace(".txt", "_formatted.txt")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(formatted_text)

    print(f"Formatted text saved to: {output_path}")
