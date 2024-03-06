
# get csv files from output folder, there should be one csv file for each vendor with the following columns:
# original_text,translated_text,reference_text,translation_time,audio_file,original_language,translated_language

# output a new csv file that contains the following:
# audio_file, deepl_bleu, google_bleu, py-translate_bleu, whisper_bleu, gladia_bleu, m2m_bleu, deepl_latency, google_latency, py-translate_latency, whisper_latency, gladia_latency, m2m_latency   
# last line should contain the average of each column

import csv

from nltk.translate.bleu_score import sentence_bleu

# How it Works: 
# BLEU measures the similarity between the machine-generated translation and the reference translations by comparing the presence and frequency of sequences of words (n-grams). 
# A higher BLEU score indicates that the machine translation is closer to the human translations, implying better quality.
# It doesn't account for the meaning of the text or grammatical correctness in a broader sense.
def calculate_bleu_score(hypothesis, reference):
    """
    Calculate the BLEU score between a hypothesis (machine-translated text) and a reference (human-translated text).

    Parameters:
    hypothesis (str): The machine-translated text.
    reference (str): The human-translated (reference) text.

    Returns:
    float: The BLEU score.
    """

    score = sentence_bleu([reference.split()], hypothesis.split())
    return score

def main():
    vendors = ['deepl', 'google', 'py-translate', 'whisper', 'gladia', 'm2m']
    results = {}

    # Initialize results dictionary
    for vendor in vendors:
        with open(f'output/{vendor}.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                audio_file = row['audio_file']
                bleu_score = calculate_bleu_score(row['translated_text'], row['reference_text'])
                latency = float(row['translation_time'])

                if audio_file not in results:
                    results[audio_file] = {'bleu_scores': {}, 'latencies': {}}
                results[audio_file]['bleu_scores'][vendor] = bleu_score
                results[audio_file]['latencies'][vendor] = latency

    with open('output/summary.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['audio_file'] + [f'{vendor}_bleu' for vendor in vendors] + [f'{vendor}_latency' for vendor in vendors]
        writer.writerow(header)

        for audio_file, data in results.items():
            row = [audio_file]
            row += [data['bleu_scores'].get(vendor, '') for vendor in vendors]
            row += [data['latencies'].get(vendor, '') for vendor in vendors]
            writer.writerow(row)

        # Calculate and write averages (if needed, handle cases where some data might be missing)
        averages = ['average']
        for vendor in vendors:
            vendor_bleu_scores = [data['bleu_scores'].get(vendor, 0) for data in results.values() if vendor in data['bleu_scores']]
            averages.append(sum(vendor_bleu_scores) / len(vendor_bleu_scores) if vendor_bleu_scores else '')
        for vendor in vendors:
            vendor_latencies = [data['latencies'].get(vendor, 0) for data in results.values() if vendor in data['latencies']]
            averages.append(sum(vendor_latencies) / len(vendor_latencies) if vendor_latencies else '')
        writer.writerow(averages)

if __name__ == '__main__':
    main()