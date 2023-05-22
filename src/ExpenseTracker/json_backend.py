import json

def load_json(file_name):
    with open(filename, 'r') as file:
        return json.load(file)

def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)