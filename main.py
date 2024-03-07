from vendors.deepl import translate as deepl_translate
from vendors.google_translate import translate as google_translate
from vendors.m2m import translate as m2m_translate
from vendors.py_translate import translate as py_translate
from vendors.gladia import translate as gladia_translate
from vendors.whisper import translate as whisper_translate

from dataset import get_dataset

import csv
import os

def write_to_csv(vendor, data):
    # Create the output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)

    filename = f"output/{vendor}.csv"

    # Check if file exists
    file_exists = os.path.isfile(filename)

    # Open the file in append mode if it exists, otherwise in write mode
    mode = 'a' if file_exists else 'w'

    with open(filename, mode, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            # Write the header if the file didn't exist
            writer.writeheader()
        writer.writerow(data)

# inputs to audio vendors
    # - audio file path
    # - language code of original text
    # - language code of target text

# inputs to text vendors
    # - original text (dataset)
    # - language code of original text
    # - language code of target text
    
# for each vendor we want to output a csv file that contains the following:
#     - the original text (from the dataset)
#     - the translated text (from the vendor)
#     - the reference text (from the dataset)
#     - the time it took to translate the text
#     - the audio file that was used to translate the text
#     - the language code of the original text
#     - the language code of the translated text

def generate_outputs_for_file(audio_path, orig_text, ref_text):
    ### Audio vendors

    if 'gladia' in VENDORS:
        try:
            gladia_out, gladia_latency = gladia_translate(audio_path, FROM_LANG, TARGET_LANG)
            write_to_csv('gladia', {
                'original_text': orig_text,
                'translated_text': gladia_out,
                'reference_text': ref_text,
                'translation_time': gladia_latency,
                'audio_file': audio_path,
                'original_language': FROM_LANG,
                'translated_language': TARGET_LANG,
            })
        except Exception as e:
            print(e)

    if 'whisper' in VENDORS:
        try:
            whisper_out, whisper_latency = whisper_translate(audio_path)
            write_to_csv('whisper', {
                'original_text': orig_text,
                'translated_text': whisper_out,
                'reference_text': ref_text,
                'translation_time': whisper_latency,
                'audio_file': audio_path,
                'original_language': FROM_LANG,
                'translated_language': TARGET_LANG,
            })
        except Exception as e:
            print(e)

    ### Text vendors
    
    if 'deepl' in VENDORS:
        try:
            deepl_out, deepl_latency = deepl_translate(orig_text, TARGET_LANG)
            write_to_csv('deepl', {
                'original_text': orig_text,
                'translated_text': deepl_out,
                'reference_text': ref_text,
                'translation_time': deepl_latency,
                'audio_file': audio_path,
                'original_language': FROM_LANG,
                'translated_language': TARGET_LANG,
            })
        except Exception as e:
            print(e)
    
    if 'google' in VENDORS:
        try:
            google_out, google_latency = google_translate(orig_text, TARGET_LANG)
            write_to_csv('google', {
                'original_text': orig_text,
                'translated_text': google_out,
                'reference_text': ref_text,
                'translation_time': google_latency,
                'audio_file': audio_path,
                'original_language': FROM_LANG,
                'translated_language': TARGET_LANG,
            })
        except Exception as e:
            print(e)
        
    if 'py-translate' in VENDORS:
        try:
            py_trans_out, py_trans_latency = py_translate(orig_text, TARGET_LANG, FROM_LANG)
            write_to_csv('py-translate', {
                'original_text': orig_text,
                'translated_text': py_trans_out,
                'reference_text': ref_text,
                'translation_time': py_trans_latency,
                'audio_file': audio_path,
                'original_language': FROM_LANG,
                'translated_language': TARGET_LANG,
            })
        except Exception as e:
            print(e)

    if 'm2m' in VENDORS:
        try:
            m2m_out, m2m_latency = m2m_translate(orig_text, TARGET_LANG, FROM_LANG)
            write_to_csv('m2m', {
                'original_text': orig_text,
                'translated_text': m2m_out,
                'reference_text': ref_text,
                'translation_time': m2m_latency,
                'audio_file': audio_path,
                'original_language': FROM_LANG,
                'translated_language': TARGET_LANG,
            })
        except Exception as e:
            print(e)

VENDORS = [
    'gladia', 
    'm2m', 
    'whisper', 
    'deepl', 
    'google', 
    'py-translate'
]

FROM_LANG = 'es'
TARGET_LANG = 'en'

def main():
    dataset = get_dataset()
    files = dataset['train']
   
    for index, f in enumerate(files):
        audio_path = f['file']
        orig_text = f['sentence']
        ref_text = f['translation']
        generate_outputs_for_file(audio_path, orig_text, ref_text)
        
if __name__ == "__main__":
    main()