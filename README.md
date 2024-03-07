# Translation Benchmarks

This project benchmarks different translation services on the CoVoST dataset. The goal is to compare the quality of translations provided by different vendors along with average latency. The quality is measured using BLEU scores.

Current vendors include:
- [Google Cloud Translation](https://cloud.google.com/translate/docs/reference/libraries/v2/python)
- [DeepL](https://www.deepl.com/en/docs-api)
- [OpenAI Whisper (STT + Translation)](https://openai.com/docs/)
- [Gladia (STT + Translation)](https://docs.gladia.io/reference/)
- [Python `translate` library](https://github.com/terryyin/translate-python) using [MyMemory](https://mymemory.translated.net/) API
- [Meta's m2m100-1.2b](https://about.fb.com/news/2020/10/first-multilingual-machine-translation-model/) (self-hosted on [Cloudflare Workers](https://developers.cloudflare.com/workers-ai/models/translation/))

Follow the steps below to run the benchmarks:

## Setup

1. **Download Common Voice and generate splits**: Follow the steps provided [here](https://github.com/facebookresearch/covost?tab=readme-ov-file#covost-2).

2. **Install the requirements**: Run `pip install -r requirements.txt` in your terminal.

3. **Add .env file with the following variables**: Make sure you have the API keys for the services you want to benchmark. The .env file should contain:

    - `DEEPL`: DeepL API key
    - `ASSEMBLY`: AssemblyAI API key
    - `GOOGLE_APPLICATION_CREDENTIALS`: Path to Google Cloud credentials
    - `OPENAI`: OpenAI API key
    - `GLADIA`: Gladia API key
    - `COMMONVOICE_DIR`: Path to Common Voice dataset

## Configuration

1. Update `VENDORS` in `main.py`: Add the list of vendors you want to use.

2. Update `FROM_LANG` and `TO_LANG` in `main.py`: Specify the language pair you want to use.

## Running the Benchmarks

1. **Generate translations**: Run `python main.py` in your terminal. This will generate translations for each vendor.

2. **Calculate BLEU scores**: Run `python calculations.py` in your terminal. This will calculate BLEU scores for each vendor.

## Results

The outputs will be saved in the `outputs` folder. There will be a CSV file for each vendor.

## More info on CoVoST
[CoVoST](https://github.com/facebookresearch/covost), a large-scale multilingual ST corpus based on Common Voice, to foster ST research with the largest ever open dataset. Its latest version covers translations from English into 15 languages---Arabic, Catalan, Welsh, German, Estonian, Persian, Indonesian, Japanese, Latvian, Mongolian, Slovenian, Swedish, Tamil, Turkish, Chinese---and from 21 languages into English, including the 15 target languages as well as Spanish, French, Italian, Dutch, Portuguese, Russian. It has total 2,880 hours of speech and is diversified with 78K speakers.

## More info on BLEU scores
BLEU measures the similarity between the machine-generated translation and the reference translations by comparing the presence and frequency of sequences of words (n-grams). 

A higher BLEU score indicates that the machine translation is closer to the human translations, implying better quality.

It doesn't account for the meaning of the text or grammatical correctness in a broader sense.