import requests
import re
import tiktoken

# Local LLM API endpoint and model configuration
API_URL = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "mistral"

def split_text_by_tokens(text, max_tokens=300):
    """
    Splits the text into chunks that do not exceed the token limit.
    If a single sentence exceeds the limit, it will be broken into smaller parts.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    sentences = re.split(r'(?<=[.؟!])\s+', text.strip())

    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = enc.encode(sentence)
        token_count = len(sentence_tokens)
        print(f"🟨 Sentence preview: '{sentence[:50]}...' | Tokens: {token_count}")

        if token_count > max_tokens:
            print(f"⚠️ Sentence too long ({token_count} tokens), splitting manually...")
            # تقسيم الجملة الطويلة إلى قطع أصغر:
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

    print(f"✅ Total chunks: {len(chunks)}")
    return chunks


def format_text_to_paragraphs(raw_text: str) -> str:
    enc = tiktoken.get_encoding("cl100k_base")

    # Safe token size to avoid exceeding 4096 context limit with prompt overhead
    chunks = split_text_by_tokens(raw_text, max_tokens=300)
    print(f"🔹 Text split into {len(chunks)} chunks.")

    formatted_chunks = []

    for idx, chunk in enumerate(chunks):
        print(f"\n🧠 Formatting chunk {idx+1}/{len(chunks)}...")

        prompt = f"""Please format the following transcribed text into clear, readable German paragraphs with correct punctuation:

---
{chunk}
---
"""
        prompt_tokens = len(enc.encode(prompt))
        print(f"🔢 Prompt tokens: {prompt_tokens}")

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
            "max_tokens": 512
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

# 🔸 Entry point when running directly
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("🔸 Usage: python format_text.py <input_file.txt>")
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    formatted_text = format_text_to_paragraphs(raw_text)

    output_path = input_path.replace(".txt", "_formatted.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(formatted_text)

    print(f"\n✅ Formatted text saved to: {output_path}")
