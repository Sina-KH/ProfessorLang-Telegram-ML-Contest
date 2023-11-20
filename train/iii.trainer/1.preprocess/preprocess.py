from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import os
import json
import re
import numpy as np
import joblib

# Load languages
with open('../../i.dataset/1.languageExtensions.json', 'r') as file:
    languages_data = json.load(file)

# Create a dictionary with language as key and index as value
lang_index = {entry['lang']: index for index, entry in enumerate(languages_data)}

# Load JSON file for keywords
with open('../../i.dataset/11.keywords/keywords.json', 'r') as json_file:
    keywords_dict = json.load(json_file)

# Load JSON file for keywords
with open('../../i.dataset/11.keywords/keywords_lang_by_lang.json', 'r') as json_file:
    keywords_2 = json.load(json_file)

# Sort keywords by length in descending order
keywords_dict_value = [value for values in keywords_dict.values() for value in values]
keywords_dict_value.extend(keywords_2)

unique_keywords = list(set(keywords_dict_value))
ready_keywords = sorted(unique_keywords, key=lambda x: len(x), reverse=True)
print(str(len(ready_keywords)) + ' keywords found')

# Save the top keywords to a JSON file
with open("./used_keywords.json", 'w') as json_file:
    json.dump(ready_keywords, json_file)

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

    #print(source_code)

    return source_code


def tokenize_to_text(source_code):
    # Define a regular expression pattern to match words and symbols
    pattern = r'\b\w+\b|[^\w\s]'

    # Use re.findall to find all matches of the pattern in the source code
    tokens = re.findall(pattern, remove_comments(source_code)[:4096])

    #print(tokens)

    return tokens


def tokenized_to_keywords(text):

    text_tokens = tokenize_to_text(text)

    # Replace keywords in the text
    indexes = []
    #debug = []
    for token in text_tokens:
        if token in ready_keywords:
            if indexes:
                last_item = indexes[-1]
                if last_item != ready_keywords.index(token) + 1:
                    indexes.append(ready_keywords.index(token) + 1)
                    #debug.append(token)
            else:
                indexes.append(ready_keywords.index(token) + 1)
                #debug.append(token)
        #else:
            #indexes.append(0)
        if len(indexes) == 200:
            break

    #print(debug)

    return indexes


# Define the path to your dataset folder
dataset_folder = "../../i.dataset/10.sampleFiles/train"
preprocessed_path = "../2.preprocessedData/"

# Loop through each folder (tag) in the dataset
for tag_folder in os.listdir(dataset_folder):
    if tag_folder not in lang_index:
        continue

    # Ensure the directory exists, create it if not
    directory = os.path.dirname(preprocessed_path + tag_folder + "/")
    if not os.path.exists(directory):
        os.makedirs(directory)

    lang_tag = lang_index[tag_folder]
    #if lang_tag > 2:
    #    continue
    print("working on " + tag_folder + " as tag " + str(lang_tag))
    tag_path = os.path.join(dataset_folder, tag_folder)

    # Ensure the item in the folder is a directory
    if os.path.isdir(tag_path):
        # Loop through each file in the folder
        for file_name in os.listdir(tag_path):
            file_path = os.path.join(tag_path, file_name)

            # Read the array from each file
            with open(file_path, 'r', errors='ignore') as file:
                data = tokenized_to_keywords(file.read())
                if len(data) < 10 and tag_folder != 'OTHER':
                    continue
                with open(os.path.join(preprocessed_path, tag_folder + "/" + file_name), 'w') as json_file:
                    json.dump(data, json_file)
                    #print(tag_folder)