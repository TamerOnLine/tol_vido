from extract_text_from_video import main as run_transcription
from format_text import format_text_to_paragraphs

def run_all():
    """
    Runs the complete process of text extraction and formatting.

    Steps:
        1. Extract text from video using the run_transcription function.
        2. Read the raw text from 'output.txt'.
        3. Format the text into readable paragraphs.
        4. Save the formatted result to 'formatted_output.txt'.
    """

    print("[1] Extracting text from video...")
    run_transcription()  # This function generates 'output.txt'

    print("[2] Formatting the text...")
    try:
        with open("output.txt", "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print("❌ Error: 'output.txt' not found. Make sure transcription succeeded.")
        return

    formatted_text = format_text_to_paragraphs(raw_text)

    with open("formatted_output.txt", "w", encoding="utf-8") as file:
        file.write(formatted_text)

    print("[3] ✅ Formatted text saved to 'formatted_output.txt'")

# Entry point if this script is executed directly
if __name__ == "__main__":
    run_all()
