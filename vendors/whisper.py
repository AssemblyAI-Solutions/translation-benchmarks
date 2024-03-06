import os
from dotenv import load_dotenv
import time
from openai import OpenAI

load_dotenv()

api_token = os.environ.get('OPENAI')

client = OpenAI(api_key=api_token)

def translate(audio_path):
    audio_file= open(audio_path, "rb")

    start = time.time()
    translation = client.audio.translations.create(
        model="whisper-1", 
        file=audio_file
    )
    end = time.time()

    return translation.text, end - start