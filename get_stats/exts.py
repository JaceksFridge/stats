

import os
import json

filename = "/path/to/your/file.txt"



ext = ".json"

def exts_dict():
    exts = {}
    with open("./data/languages.json", "r") as file:
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



