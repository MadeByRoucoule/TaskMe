import json
import os

class ThemeManager:
    def __init__(self):
        self.themes_files = self.themes_path()

    def themes_path(self):
        return os.listdir('json/themes')

    def load_themes_names(self):
        themes_names = []
        for i in range(len(self.themes_files)):
            print(i)
            with open(f'json/themes/{self.themes_files[i]}', 'r') as t:
                themes_file = json.load(t)
            themes_names.append(themes_file['name'])
        return themes_names

    def change_theme(self, theme_name):
        for i in range(len(self.themes_files)):
            path = f'json/themes/{self.themes_files[i]}'
            with open(path, 'r') as t:
                themes_file = json.load(t)
            if themes_file['name'] == theme_name:
                with open('json/settings.json', 'r') as f:
                    settings = json.load(f)
                settings['current_theme'] = path
                with open('json/settings.json', 'w') as f:
                    json.dump(settings, f)

    def get_current_theme(self):
        with open('json/settings.json', 'r') as f:
                    settings = json.load(f)
        with open(settings['current_theme'], 'r') as f:
            theme = json.load(f)
            return theme['colors']