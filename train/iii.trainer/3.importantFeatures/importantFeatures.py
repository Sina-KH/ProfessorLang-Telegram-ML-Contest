from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os
import json
import re
import numpy as np
import joblib
from micromlgen import port

# Load languages
with open('../../i.dataset/1.languageExtensions.json', 'r') as file:
    languages_data = json.load(file)

# Create a dictionary with language as key and index as value
lang_index = {entry['lang']: index for index, entry in enumerate(languages_data)}

# Load JSON file for keywords
with open('../1.preprocess/used_keywords.json', 'r') as json_file:
    ready_keywords = json.load(json_file)

print(str(len(ready_keywords)) + ' keywords found')

# Save the top keywords to a JSON file
with open("./used_keywords.json", 'w') as json_file:
    json.dump(ready_keywords, json_file)

# Define the path to your dataset folder
dataset_folder = "../2.preprocessedData"

def normalize_to_100(arr):
    # Calculate the sum of the array
    total = sum(arr)
    if (total == 0):
        total = 1

    # Normalize each element
    normalized_arr = [element / total * 100 for element in arr]

    return normalized_arr

# Initialize empty lists to store features (X) and labels (y)
X = []
y = []

# Loop through each folder (tag) in the dataset
for tag_folder in os.listdir(dataset_folder):
    if tag_folder not in lang_index:
        continue
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
                file_data = json.load(file)
                x_data = np.zeros(len(ready_keywords) + 1)
                for i in file_data:
                    x_data[i] += 1
                if (sum(x_data) < 10 and lang_tag != 'OTHER'):
                    continue
                X.append(normalize_to_100(x_data))
                y.append(lang_tag)  # Convert tag folder name to integer

# Find the maximum sequence length
max_len = max(len(seq) for seq in X)

# Pad sequences to ensure consistent length
# X = np.array([seq + [0] * (max_len - len(seq)) for seq in X])

# Now, X contains the features (arrays) and y contains the corresponding labels (tags)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the classifier
#clf = SVC(verbose=True, max_iter=10)  # You can try different kernels like 'rbf' or 'poly'
clf = RandomForestClassifier(n_estimators=100, max_depth=50, min_samples_leaf=20, random_state=42, verbose=True)

# Train the model
clf.fit(X_train, y_train)

# Save the trained model to a file
model_filename = 'model.joblib'
joblib.dump(clf, model_filename)

# Make predictions on the test set
predictions = clf.predict(X_test)

# Evaluate the accuracy
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Get feature importances
feature_importances = clf.feature_importances_
print(feature_importances)

# Get indices of features sorted by importance
indices = np.argsort(feature_importances)[::-1][:2000]
print(indices)

top_k_features = []
for i in indices:
    top_k_features.append(ready_keywords[i - 1])
    if i == 0:
        print(f"Feature 0: {feature_importances[i]}")
    else:
        print(f"Feature {ready_keywords[i - 1]}: {feature_importances[i]}")

# Save the top keywords to a JSON file
with open("../4.importantFeatures.json", 'w') as json_file:
    json.dump(top_k_features, json_file)

with open('RandomForestRegressor.h', 'w') as file:
    file.write(port(clf))
