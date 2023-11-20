from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score
import os
import json
import re
import numpy as np
import joblib
from sklearn.model_selection import GridSearchCV
from micromlgen import port

# Load languages
with open('../../i.dataset/1.languageExtensions.json', 'r') as file:
    languages_data = json.load(file)

# Create a dictionary with language as key and index as value
lang_index = {entry['lang']: index for index, entry in enumerate(languages_data)}

# Load JSON file for keywords
with open('../FINAL_KEYWORDS.json', 'r') as json_file:
    ready_keywords = json.load(json_file)

print(str(len(ready_keywords)) + ' keywords found')

# TEST

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
    tokens = re.findall(pattern, remove_comments(source_code))

    #print(tokens)

    return tokens


def tokenized_to_keywords(text):

    text_tokens = tokenize_to_text(text)

    # Replace keywords in the text
    indexes = []
    debug = []

    for token in text_tokens:
        exists = token in ready_keywords
        if not exists:
            exists = token.lower() in ready_keywords
            if exists:
                token = token.lower()
# we lowercased all fully-uppsercased keywords in 5.reprocessor
#             elif not exists:
#                 exists = token.upper() in ready_keywords
#                 if exists:
#                     token = token.upper()

        if exists:
            if indexes:
                last_item = indexes[-1]
                if last_item != ready_keywords.index(token) + 1:
                    indexes.append(ready_keywords.index(token) + 1)
                    debug.append(token)
            else:
                indexes.append(ready_keywords.index(token) + 1)
                debug.append(token)
        else:
            if indexes:
                last_item = indexes[-1]
                if last_item != 0:
                    indexes.append(0)
                    debug.append(token)
            else:
                indexes.append(0)
                debug.append(token)

        if len(indexes) == 200:
            break

    #print(debug)

    return indexes


def normalize_to_100(arr):
    # Calculate the sum of the array
    total = sum(arr)
    if total == 0:
        total = 1

    # Normalize each element
    normalized_arr = [element / total * 100 for element in arr]

    return normalized_arr


# Load the saved model
model_path = './model.joblib'
model = joblib.load(model_path)

X = []
y_valid = []

# Loop through each folder (tag) in the validate folder
valid_folder = "../../v.test/valid/"

for tag_folder in os.listdir(valid_folder):
    if tag_folder not in lang_index:
        continue
    lang_tag = lang_index[tag_folder]
    #if lang_tag > 2:
    #    continue
    # print("working on " + tag_folder + " as tag " + str(lang_tag))
    tag_path = os.path.join(valid_folder, tag_folder)

    # Ensure the item in the folder is a directory
    if os.path.isdir(tag_path):

        X_tag = []
        y_valid_tag = []

        # Loop through each file in the folder
        for file_name in os.listdir(tag_path):
            file_path = os.path.join(tag_path, file_name)

            # Read the array from each file
            with open(file_path, 'r', errors='ignore') as file:
                x_data = np.zeros(len(ready_keywords) + 1)
                for i in tokenized_to_keywords(file.read()):
                    x_data[i] = x_data[i] + 1
                norm = normalize_to_100(x_data)
                X.append(norm)
                y_valid.append(lang_tag)
                X_tag.append(norm)
                y_valid_tag.append(lang_tag)

        if (len(X_tag) == 0):
            continue
        predictions = model.predict(X_tag)
        # Evaluate the accuracy for tag
        accuracy = accuracy_score(y_valid_tag, predictions)
        print(f'Accuracy for {tag_folder}: {accuracy * 100:.2f}%')
        if (accuracy < 0.9):
            print([p for p in predictions if p != lang_tag][:10])


predictions = model.predict(X)

# Evaluate the accuracy
accuracy = accuracy_score(y_valid, predictions)
print(f'Accuracy: {accuracy * 100:.2f}%')
