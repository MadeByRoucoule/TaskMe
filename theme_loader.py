import json

class ThemeManager:
    def __init__(self):
        self.current_theme_name = ''
        self.current_theme_path = ''
        self.themes = self.load_themes()
        self.load_current_theme()
    
    def load_themes(self):
        with open('themes.json', 'r') as s:
            themes_file = json.load(s)
        return themes_file['themes']

    def load_current_theme(self):
        try:
            with open('settings.json', 'r') as s:
                settings = json.load(s)
                self.set(settings['current_theme'])
        except (FileNotFoundError, json.JSONDecodeError):
            print("Using default theme.")
            self.set("Default Dark")

    def save_current_theme(self):
        settings = {'current_theme': self.current_theme_name}
        with open('settings.json', 'w') as s:
            json.dump(settings, s, indent=4)

    def set(self, new_theme_name):
        for theme in self.themes:
            if theme['name'].lower() == new_theme_name.lower():
                self.current_theme_name = theme['name']
                self.current_theme_path = theme['path']
                self.save_current_theme()
                return self.current_theme_path
        
        print(f"Theme '{new_theme_name}' not found.")
        return None

    def get_current_theme(self):
        with open(self.current_theme_path, 'r') as f:
            return json.load(f)