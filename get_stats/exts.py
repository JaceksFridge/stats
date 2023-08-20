

import os
import json


ext = ".json"

def exts_dict():
    # Find the directory where the current script (exts.py) is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the languages.json file based on the directory of exts.py
    languages_json_path = os.path.join(current_dir, "data", "languages.json")
    exts = {}
    with open(languages_json_path, "r") as file:
        data = json.load(file)
        
        for language in data:
            try:
                if len(language['extensions']) == 1:
                    exts[language['extensions'][0]] = language['name']
                elif len(language['extensions']) > 1:
                    for ext in language['extensions']:
                        exts[ext] = language['name']
            except KeyError:
                continue
    return exts



