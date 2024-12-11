import json

class SettingsManager:
    def __init__(self):
        self.settings_file_path = 'json/settings.json'

    def load_settings(self):
        with open(self.settings_file_path, 'r') as f:
            return json.load(f)