## Meta's M2M model (Cloudflare AI Workers)
# Note: This is an open source translation model that supports 50+ languages. It will need to be hosted on your own server. For this demo, I have set up a Cloudflare Worker test function that hosts the M2M model.
  
# Meta's M2M Paper: https://about.fb.com/news/2020/10/first-multilingual-machine-translation-model/
# HuggingFace: https://huggingface.co/facebook/m2m100_418M
# Cloudflare AI: https://developers.cloudflare.com/workers-ai/models/translation/

import requests
import os
import time

def translate(transcript_id, target_lang, from_lang='en'):
    start = time.time()
    r = requests.get(f'https://m2m-translate.neil-88b.workers.dev/?text={transcript_id}&target_lang={target_lang}&from_lang={from_lang}')
    translated_text = r.json()['translated_text']
    end = time.time()

    return translated_text, end - start