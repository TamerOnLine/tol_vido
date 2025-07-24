import requests
import re
import tiktoken

# Local LLM API endpoint and model configuration
API_URL = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "mistral"

def split_text_by_tokens(text, max_tokens=1500):
    """
    Splits the text into chunks that do not exceed the token limit.
    Uses tiktoken with cl100k_base tokenizer and splits on sentence endings.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    sentences = re.split(r'(?<=[.؟!])\s+', text.strip())

    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(enc.encode(sentence))

        if current_tokens + sentence_tokens <= max_tokens:
            current_chunk += sentence + " "
            current_tokens += sentence_tokens
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
            current_tokens = sentence_tokens

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def format_text_to_paragraphs(raw_text: str) -> str:
    """
    Sends raw transcribed text to a local LLM server in safe chunks,
    then combines and returns the formatted version.
    """
    chunks = split_text_by_tokens(raw_text, max_tokens=1500)
    print(f"🔹 Text split into {len(chunks)} chunks.")

    formatted_chunks = []

    for idx, chunk in enumerate(chunks):
        print(f"🧠 Formatting chunk {idx+1}/{len(chunks)}...")

        prompt = f"""Please format the following transcribed text into clear, readable German paragraphs with correct punctuation:

---
{chunk}
---
"""

        response = requests.post(API_URL, json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a German editor who formats transcripts into readable, well-punctuated text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.6,
            "max_tokens": 2048
        })

        if response.status_code == 200:
            formatted = response.json()["choices"][0]["message"]["content"]
            formatted_chunks.append(formatted.strip())
        else:
            try:
                error_msg = response.json().get("error", {}).get("message", response.text)
            except:
                error_msg = response.text
            raise Exception(f"\n❌ LLM API Error {response.status_code}:\n{error_msg}")

    return "\n\n".join(formatted_chunks)
