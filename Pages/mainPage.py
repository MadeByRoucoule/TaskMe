import tkinter as tk
import random
import widgets
from Managers.tasksManager import TasksManager

class MainPage:
    def __init__(self, parent, theme):
        
        self.parent = parent
        self.theme = theme

        self.frames()
        
        
        # tm.get_tasks_infos()

    def frames(self):

        # -- Top Section -- #
        self.top_frame = tk.Frame(self.parent, bg=self.theme['top_frame'], width=1000, height=50)
        self.top_frame.pack(side='top')

        # -- Bottom Section -- #
        self.bottom_frame = tk.Frame(self.parent, width=1000, height=550)
        self.bottom_frame.pack(side='bottom', fill='both', expand=True)

        # -- Left Frame -- #
        self.left_frame = tk.Frame(self.bottom_frame, bg=self.theme['left_frame'], width=210)
        self.left_frame.pack(side='left', fill='y')
        
        # -- Main Frame -- #
        self.main_frame = tk.Frame(self.bottom_frame, bg=self.theme['main_frame'])
        self.main_frame.pack(side='right', fill='both', expand=True)

        btn = widgets.Button(self.left_frame, text='Add Task', color=self.theme['colored_button'], hover_color=self.theme['hover_colored_button'], width=190, font=('San Francisco', 10, 'bold'), command=self.btn)
        btn.place(x=10, y=510)

        task_manager = TasksManager()
        tasks = task_manager.load_tasks()

        y = 10
        x = 10
        tasks_per_row = 3

        for task in tasks['tasks']:

            w = widgets.TaskWidget(self.main_frame, text=task['text'], date=task['date'], hour=task['hour'], priority=task['priority'], completed=True, fg=self.theme['fg'], priority_colors=self.theme['priority_colors'], hover_priority_colors=self.theme['hover_priority_colors'], width=250)
            w.place(x=x, y=y)
            tasks_per_row -= 1
            if tasks_per_row == 0:
                y = y + 100 + 10
                x = 10
                tasks_per_row = 3
            else:
                x = x + 250 + 10
            

    def btn(self):
        print('Pressed')