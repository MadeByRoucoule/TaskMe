import json

class TasksManager:
    def __init__(self):
        self.tasks_file_path = 'json/tasks.json'

    def load_tasks(self):
        with open(self.tasks_file_path, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        return tasks

    def get_task_info(self, text):
        infos = []
        tasks = self.load_tasks()
        for task in tasks['tasks']:
            if task['text'] == text:
                infos.append(task['text'])
                infos.append(task['date'])
                infos.append(task['hour'])
                infos.append(task['priority'])
                return infos