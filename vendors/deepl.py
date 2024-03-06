## DeepL API
# https://www.deepl.com/en/docs-api

import deepl
from dotenv import load_dotenv
import os
import time

load_dotenv()
TOKEN = os.getenv('DEEPL')

def translate(text, target_lang='EN-US'):
    translator = deepl.Translator(TOKEN)

    if target_lang == 'en':
        target_lang = 'EN-US'

    start = time.time()
    result = translator.translate_text(text, target_lang=target_lang) # Note: DeepL requires more formal language code
    end = time.time()
    
    return result.text, end - start