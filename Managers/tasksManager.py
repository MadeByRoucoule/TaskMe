import json
from datetime import datetime, date

class TasksManager:
    def __init__(self):
        self.tasks_file_path = 'json/tasks.json'

    def load_tasks(self):
        with open(self.tasks_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_task_info(self, text):
        tasks = self.load_tasks()
        for task in tasks['tasks']:
            if task['text'] == text:
                return [task['text'], task['date'], task['hour'], task['priority'], task['note']]
        return []

    def add_task(self, text, date, hour, priority):
        with open(self.tasks_file_path, 'r+', encoding='utf-8') as f:
            tasks = json.load(f)
            new_task = {
                'text': text,
                'date': date,
                'hour': hour,
                'priority': priority,
                'note':''
            }
            tasks['tasks'].append(new_task)
            f.seek(0)
            json.dump(tasks, f, indent=4)

    def save_task(self, tasks):
        with open(self.tasks_file_path, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4)

    def delete_task(self, text):
        with open(self.tasks_file_path, 'r+', encoding='utf-8') as f:
            tasks = json.load(f)
            tasks['tasks'] = [task for task in tasks['tasks'] if task['text'] != text]
            f.seek(0)
            f.truncate()
            json.dump(tasks, f, indent=4)

    def get_sorted_tasks(self, tab, sort_options):
        tasks = self.load_tasks()['tasks']
        filtered_tasks = self.filter_tasks(tasks, tab)
        return self.sort_tasks(filtered_tasks, sort_options)

    def filter_tasks(self, tasks, tab):
        today = datetime.now().date()
        if tab == 'All':
            return tasks
        elif tab == 'Today':
            return [task for task in tasks if self.parse_date(task['date']) == today]
        elif tab == 'Later':
            return [task for task in tasks if self.parse_date(task['date']) > today]
        elif tab == 'Before':
            return [task for task in tasks if self.parse_date(task['date']) < today]
        else:
            return []

    def sort_tasks(self, tasks, sort_options):
        def sort_key(task):
            keys = []
            for option in sort_options:
                if option == "Time":
                    keys.append(self.parse_datetime(task['date'], task['hour']))
                elif option == "Priority":
                    priority_order = {"High": 0, "Medium": 1, "Low": 2}
                    keys.append(priority_order.get(task['priority'], 3))
            return tuple(keys)

        return sorted(tasks, key=sort_key)

    @staticmethod
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            return datetime.min.date()

    @staticmethod
    def parse_datetime(date_str, time_str):
        try:
            time_str = time_str.replace('h', ':')
            return datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
        except ValueError:
            return datetime.min