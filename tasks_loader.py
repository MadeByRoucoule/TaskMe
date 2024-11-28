import json

def load_tasks():
    try:
        with open('json/tasks.json', 'r') as file:
            data = json.load(file)
            return data['tasks']
    except FileNotFoundError:
        print("Le fichier tasks.json n'a pas été trouvé.")
        return []
    except json.JSONDecodeError:
        print("Erreur dans le format du fichier tasks.json.")
        return []
