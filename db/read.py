import json

# Load JSON data from a file
with open('./db/question1.json') as file:
    json_data = json.load(file)

# Print all attributes and values
for key, value in json_data['WMT20230331'].items():
    print(f"{key}")