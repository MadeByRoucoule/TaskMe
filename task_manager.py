import json
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open('json/tasks.json', 'r') as t:
                tasks_file = json.load(t)
            return tasks_file['tasks']
        except FileNotFoundError:
            print("Le fichier tasks.json n'a pas été trouvé. Création d'une liste de tâches vide.")
            return []
        except json.JSONDecodeError:
            print("Erreur dans le format du fichier tasks.json. Création d'une liste de tâches vide.")
            return []

    def save_tasks(self):
        with open('json/tasks.json', 'w') as t:
            json.dump({'tasks': self.tasks}, t, indent=4)

    def add_task(self, text, date, hour, priority):
        new_task = {
            "text": text,
            "date": date,
            "hour": hour,
            "priority": priority
        }
        self.tasks.append(new_task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
        else:
            print("Index de tâche invalide.")

    def get_tasks(self):
        return self.tasks

    def update_task(self, index, text=None, date=None, hour=None, priority=None):
        if 0 <= index < len(self.tasks):
            if text:
                self.tasks[index]['text'] = text
            if date:
                self.tasks[index]['date'] = date
            if hour is not None:
                self.tasks[index]['hour'] = hour
            if priority:
                self.tasks[index]['priority'] = priority
            self.save_tasks()
        else:
            print("Index de tâche invalide.")