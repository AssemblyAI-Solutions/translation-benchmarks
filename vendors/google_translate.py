## Google Translate API
# https://cloud.google.com/translate/docs/reference/libraries/v2/python

import os
from dotenv import load_dotenv
import time

load_dotenv()

# os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def translate(text: str, target_lang: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    start = time.time()
    result = translate_client.translate(text, target_language=target_lang)
    end = time.time()

    return result["translatedText"], end - start