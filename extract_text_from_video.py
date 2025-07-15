import os
from yt_dlp import YoutubeDL
import speech_recognition as sr
from pydub import AudioSegment

def download_audio(url, output_audio="audio.wav"):
    """
    Downloads audio from a YouTube video and converts it to a 16kHz mono WAV file.

    Args:
        url (str): URL of the YouTube video.
        output_audio (str): Output filename for the converted audio.

    Returns:
        str: Path to the processed audio file.
    """
    ffmpeg_path = os.path.join(os.getcwd(), "bin")

    ydl_opts = {
        'ffmpeg_location': ffmpeg_path,
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_audio.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    downloaded_file = "downloaded_audio.wav"
    if not os.path.exists(downloaded_file):
        raise Exception("Audio file not found after download.")

    sound = AudioSegment.from_wav(downloaded_file)
    sound = sound.set_frame_rate(16000).set_channels(1)
    sound.export(output_audio, format="wav")
    os.remove(downloaded_file)

    return output_audio

def split_audio(audio_path, chunk_length_ms=60000):
    """
    Splits a WAV audio file into chunks of a specified duration.

    Args:
        audio_path (str): Path to the audio file.
        chunk_length_ms (int): Duration of each chunk in milliseconds.

    Returns:
        list of str: List of file paths to the audio chunks.
    """
    sound = AudioSegment.from_wav(audio_path)
    chunks = []
    for i in range(0, len(sound), chunk_length_ms):
        chunk = sound[i:i + chunk_length_ms]
        chunk_path = f"chunk_{i // chunk_length_ms}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks

def transcribe_audio(audio_path, language="de-DE"):
    """
    Transcribes spoken content in an audio file using Google Speech Recognition.

    Args:
        audio_path (str): Path to the audio file.
        language (str): Language code for transcription.

    Returns:
        str: Transcribed text or error message.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language=language)
        except sr.UnknownValueError:
            return "[Unrecognized speech]"
        except sr.RequestError as e:
            return f"[API error: {e}]"

def main():
    """
    Main function to process a YouTube URL into transcribed text.
    """
    url = input("Enter the YouTube video URL: ").strip()
    print("Downloading and preparing audio...")
    audio_file = download_audio(url)

    print("Splitting audio into 60-second chunks...")
    chunks = split_audio(audio_file)

    print("Transcribing chunks...")
    all_text = []
    for i, chunk in enumerate(chunks):
        print(f"  Transcribing chunk {i + 1}/{len(chunks)}...")
        text = transcribe_audio(chunk, language="de-DE")
        all_text.append(text)
        os.remove(chunk)

    output_path = "output.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))

    print(f"Done! Full transcription saved to {output_path}")
    os.remove(audio_file)

if __name__ == "__main__":
    main()