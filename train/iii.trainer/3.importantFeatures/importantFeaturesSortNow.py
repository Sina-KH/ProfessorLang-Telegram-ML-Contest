# USED TO SORT IMPORTANT FEATURES BEFORE REPROCESSING

import os
import json

# Load JSON file for keywords
with open('../4.importantFeatures.json', 'r') as json_file:
    important_keywords = json.load(json_file)

ready_keywords = sorted(important_keywords, key=lambda x: len(x), reverse=True)
print(str(len(ready_keywords)) + ' keywords found')

# Save the top keywords to a JSON file
with open("../4.importantFeaturesSorted.json", 'w') as json_file:
    json.dump(ready_keywords, json_file)
