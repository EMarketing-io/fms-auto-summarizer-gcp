import openai
from audio.config import OPENAI_KEY

# 🔐 Set the OpenAI API key (loaded from .env via config)
openai.api_key = OPENAI_KEY


# 🎧 Transcribes an audio file to text using OpenAI Whisper API
def transcribe_audio(audio_path):
    print("🎙️ Transcribing with OpenAI Whisper API...")
    
    # Open the audio file in binary mode
    with open(audio_path, "rb") as audio_file:
        # 🔁 Send file to OpenAI Whisper for transcription (English translation)
        response = openai.Audio.transcribe(
            model="whisper-1",       # Use Whisper model
            file=audio_file,         # Pass the audio stream
            response_format="text",  # Return plain text
            task="translate"         # Auto-translate non-English audio to English
        )
        
        # 🧾 Return cleaned transcript
        return response.strip()