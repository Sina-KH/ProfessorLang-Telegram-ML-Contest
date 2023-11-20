import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
import json

# Download NLTK resources (you only need to do this once)
nltk.download('punkt')
nltk.download('stopwords')


def remove_comments(source_code):
    # Remove single-line comments
    source_code = re.sub(r'//.*', '', source_code)

    # Remove multi-line comments
    source_code = re.sub(r'/\*(.*?)\*/', '', source_code, flags=re.DOTALL)

    # Remove single-line comments
    source_code = re.sub(r'#.*', '', source_code)

    # Remove multi-line comments using triple-quoted strings
    source_code = re.sub(r"'''(.*?)'''", '', source_code, flags=re.DOTALL)
    source_code = re.sub(r'"""(.*?)"""', '', source_code, flags=re.DOTALL)

    source_code = re.sub(r'"[^"]*"', '""', source_code)
    source_code = re.sub(r"'[^']*'", "''", source_code)

    return source_code

# Define the path to your dataset folder
dataset_folder = "../10.sampleFiles/train"

total_items = []

# Loop through each folder (tag) in the dataset
for tag_folder in os.listdir(dataset_folder):
    dataset = []

    if (tag_folder == 'OTHER'):
        continue

    print("working on " + tag_folder)
    tag_path = os.path.join(dataset_folder, tag_folder)

    # Ensure the item in the folder is a directory
    if os.path.isdir(tag_path):
        # Loop through each file in the folder
        for file_name in os.listdir(tag_path):
            file_path = os.path.join(tag_path, file_name)

            # Read the array from each file
            with open(file_path, 'r', errors='ignore') as file:
                dataset.append(remove_comments(file.read()))

    # Tokenization
    tokens = [word_tokenize(sentence) for sentence in dataset]

    # Flatten the list of tokens
    flat_tokens = [token for sublist in tokens for token in sublist]

    # Remove stopwords
    # stop_words = set(stopwords.words('english'))
    filtered_tokens = [token.lower() for token in flat_tokens if
                       token.isalnum()]  # and token.lower() not in stop_words]

    # Frequency distribution
    freq_dist = FreqDist(filtered_tokens)
    data = freq_dist.most_common(80)
    print("Top 80 tokens by frequency:", data)

    # Extract the first items from each tuple
    first_items = [item[0] for item in data if not (item[0].isdigit() or item[0].startswith("0x") or len(item[0]) == 1)]

    # Convert the list to JSON
    total_items.extend(first_items[:35])

# Save the top keywords to a JSON file
with open("./keywords_lang_by_lang.json", 'w') as json_file:
    json.dump(total_items, json_file)