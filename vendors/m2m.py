## Meta's M2M model (Cloudflare AI Workers)
# Note: This is an open source translation model that supports 50+ languages. It will need to be hosted on your own server. For this demo, I have set up a Cloudflare Worker test function that hosts the M2M model.
  
# Meta's M2M Paper: https://about.fb.com/news/2020/10/first-multilingual-machine-translation-model/
# HuggingFace: https://huggingface.co/facebook/m2m100_418M
# Cloudflare AI: https://developers.cloudflare.com/workers-ai/models/translation/

import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()
TOKEN = os.getenv('ASSEMBLY')

### Function params
### transcript_id: str – AAI transcript_id
### target_lang: str - target language for the translation

def translate(transcript_id, target_lang):
    start = time.time()
    r = requests.get(f'https://worker-lively-firefly-6667.neil-88b.workers.dev?transcript_id={transcript_id}&target_lang={target_lang}', headers={
        'Authorization': TOKEN
    })

    translated_text = r.json()['translated_text']
    end = time.time()

    return translated_text, end - start