from datasets import load_dataset
from dotenv import load_dotenv
import os

load_dotenv()

def get_dataset():
    # End to end STT translation
    dataset = load_dataset('covost2', 'es_en', data_dir=os.getenv('COMMONVOICE_DIR'))

    # For text only translation
    # dataset = load_dataset("facebook/flores", "all")
    # print(dataset['dev'][0]['sentence_eng_Latn'])
    # print(dataset['dev'][0]['sentence_spa_Latn'])
    return dataset

# data = get_dataset()
# f = (data['train'][0])
