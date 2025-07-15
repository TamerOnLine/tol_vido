from extract_text_from_video import main as run_transcription
from format_text import format_text_to_paragraphs

def run_all():
    """
    Executes the full text extraction and formatting process.

    Steps:
        1. Extract text from video using run_transcription.
        2. Read the extracted text from 'output.txt'.
        3. Format the text into paragraphs.
        4. Save the formatted text to 'formatted_output.txt'.
    """
    print("[1] Extracting text from video...")
    run_transcription()  # This will generate 'output.txt'

    print("[2] Formatting the text...")
    with open("output.txt", "r", encoding="utf-8") as file:
        raw_text = file.read()

    formatted_text = format_text_to_paragraphs(raw_text)

    with open("formatted_output.txt", "w", encoding="utf-8") as file:
        file.write(formatted_text)

    print("[3] Formatted text saved to 'formatted_output.txt'")

if __name__ == "__main__":
    run_all()