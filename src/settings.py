import json

with open('settings.json') as data_file:
    _settings = json.load(data_file)

settings = _settings
