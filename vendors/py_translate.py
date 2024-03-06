## `translate-python` Library
# https://github.com/terryyin/translate-python

from translate import Translator
import time

def translate(text, target_lang, from_lang):
    translator = Translator(to_lang=target_lang, from_lang=from_lang)

    start = time.time()
    translation = translator.translate(text)
    end = time.time()

    return translation, end - start