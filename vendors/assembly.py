import assemblyai as aai
from dotenv import load_dotenv
import os

load_dotenv()

AAI_API_TOKEN = os.getenv("ASSEMBLY")

# set the API key
aai.settings.api_key = f"{AAI_API_TOKEN}"

def transcribe(file_path, language='en'):
    config = aai.TranscriptionConfig(language_code=language)
    transcriber = aai.Transcriber(config=config)

    t = transcriber.transcribe(file_path)
    return t.id