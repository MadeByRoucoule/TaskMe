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
            
    def add_task(self, text, date, hour, priority):
        with open(self.tasks_file_path, 'r+', encoding='utf-8') as f:
            tasks = json.load(f)
            new_task = {
                'text':text,
                'date':date,
                'hour':hour,
                'priority':priority
            }
            tasks['tasks'].append(new_task)
            f.seek(0)
            json.dump(tasks, f, indent=4)
            