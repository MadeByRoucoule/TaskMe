import json

class TasksManager:
    def __init__(self):
        self.tasks_file_path = 'json/tasks.json'

    def load_tasks(self):
        with open(self.tasks_file_path, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        return tasks

    def get_tasks_infos(self):
        self.load_tasks()
        for task in self.tasks['tasks']:
            print(task['text'])