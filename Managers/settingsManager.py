import json

class SettingsManager:
    def __init__(self):
        self.settings_file_path = 'json/settings.json'

    def load_settings(self):
        try:
            with open(self.settings_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_settings(self, settings):
        with open(self.settings_file_path, 'w') as f:
            json.dump(settings, f, indent=4)
