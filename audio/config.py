# 📦 Standard Library
import os

# 🌐 Load environment variables from .env file into the environment
from dotenv import load_dotenv

# 🔐 Load all environment variables at runtime
load_dotenv()

# 🔑 OpenAI API key — used for Whisper and GPT calls
OPENAI_KEY = os.getenv("OPENAI_KEY")

# 📁 Folder ID in Google Drive where processed audio summaries should be uploaded
AUDIO_DRIVE_FOLDER_ID = os.getenv("AUDIO_DRIVE_FOLDER_ID")