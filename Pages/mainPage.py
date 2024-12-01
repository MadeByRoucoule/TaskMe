import tkinter as tk
import platform
if platform.system() == 'Windows':
    from hPyT import *
import widgets
from Managers.tasksManager import TasksManager

class MainPage:
    def __init__(self, parent, theme):
        
        self.parent = parent
        self.theme = theme

        self.frames()
        self.widgets()

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

    def widgets(self):

        btn = widgets.Button(self.left_frame, text='Add Task', color=self.theme['green_button'], hover_color=self.theme['hover_green_button'], width=190, font=('San Francisco', 10, 'bold'), command=self.add_task)
        btn.place(x=10, y=510)

        priority_btn = widgets.MenuButton(self.left_frame, color=self.theme["menu_button"], hover_color=self.theme["hover_menu_button"], fg=self.theme['fg'], width=190)
        priority_btn.place(x=10, y=10)

        self.update_tasks_widgets()

    def update_tasks_widgets(self):
        try:
            self.w.place_forget()
        except:
            None
        task_manager = TasksManager()
        tasks = task_manager.load_tasks()
        y = 10
        x = 10
        tasks_per_row = 3
        for task in tasks['tasks']:
            self.w = widgets.TaskWidget(self.main_frame, radius=25, text=task['text'], date=task['date'], hour=task['hour'], priority=task['priority'], completed=True, fg=self.theme['fg'], priority_colors=self.theme['priority_colors'], hover_priority_colors=self.theme['hover_priority_colors'], width=250, tag=task['text'], command=lambda t=task['text']: self.open_task_window(t))
            self.w.place(x=x, y=y)
            tasks_per_row -= 1
            if tasks_per_row == 0:
                y = y + 100 + 10
                x = 10
                tasks_per_row = 3
            else:
                x = x + 250 + 10

    # -- ADD TASK WINDOW -- #
    def add_task(self):

        width, height = 250, 250
        posx, posy = ( self.parent.winfo_x() + self.parent.winfo_width()//2 ) - width // 2, ( self.parent.winfo_y() + self.parent.winfo_height()//2 ) - height // 2
        priority = ['High', 'Medium', 'Low']

        self.add_task_win = tk.Toplevel(self.parent, bg=self.theme['top_frame'])
        self.add_task_win.title('Add·Task')
        self.add_task_win.geometry(f'{width}x{height}+{posx}+{posy}')
        self.add_task_win.resizable(False, False)

        if platform.system() == 'Windows':
            all_stuffs.hide(self.add_task_win)
            title_bar_color.set(self.add_task_win, self.theme['title_bar'])

        self.name_entry = widgets.Entry(self.add_task_win, color=self.theme["entry"], border_color=self.theme['entry_border'], placeholder_text='Name', width=200)
        self.name_entry.pack(pady=(10,5))
        self.date_entry = widgets.Entry(self.add_task_win, color=self.theme["entry"], border_color=self.theme['entry_border'], placeholder_text='Date (d/m/y)', width=200)
        self.date_entry.pack(pady=5)
        self.hour_entry = widgets.Entry(self.add_task_win, color=self.theme["entry"], border_color=self.theme['entry_border'], placeholder_text='Hour (ex: 12h00)', width=200)
        self.hour_entry.pack(pady=5)
        self.priority_btn = widgets.MenuButton(self.add_task_win, color=self.theme["menu_button"], hover_color=self.theme["hover_menu_button"], fg=self.theme['fg'], width=200)
        self.priority_btn.pack(pady=5)

        self.cancel_btn = widgets.Button(self.add_task_win, text='Cancel', color=self.theme['red_button'], hover_color=self.theme['hover_red_button'], width=200,command=lambda: self.add_task_win.destroy())
        self.cancel_btn.pack(side='bottom', pady=(5,10))
        self.done_btn = widgets.Button(self.add_task_win, text='Done', color=self.theme['green_button'], hover_color=self.theme['hover_green_button'], width=200,command=self.add_task_done)
        self.done_btn.pack(side='bottom', pady=5)

    def add_task_done(self):

        task_manager = TasksManager()
        task_manager.add_task(self.name_entry.get(), self.date_entry.get(), self.hour_entry.get(), 'Low')
        self.update_tasks_widgets()
        self.add_task_win.destroy()

    # -- TASK WINDOW -- #
    def open_task_window(self, tag):

        task_manager = TasksManager()
        width, height = 400, 500
        posx, posy = (self.parent.winfo_x() + self.parent.winfo_width()//2) - width // 2, (self.parent.winfo_y() + self.parent.winfo_height()//2) - height // 2
        infos = task_manager.get_task_info(tag)

        self.task_win = tk.Toplevel(self.parent, bg=self.theme['top_frame'])
        self.task_win.title('Task Details')
        self.task_win.geometry(f'{width}x{height}+{posx}+{posy}')
        self.task_win.resizable(False, False)

        if platform.system() == 'Windows':
            all_stuffs.hide(self.task_win)
            title_bar_color.set(self.task_win, self.theme['title_bar'])

        self.task_win.bind("<FocusOut>", lambda e: self.close_task_window())

        tk.Label(self.task_win, text=infos[0], font=('San Francisco', 16, 'bold'), bg=self.theme['top_frame'], fg=self.theme['fg']).pack(pady=10)
        tk.Label(self.task_win, text=f"Date: {infos[1]}", bg=self.theme['top_frame'], fg=self.theme['fg']).pack(pady=5)
        tk.Label(self.task_win, text=f"Heure: {infos[2]}", bg=self.theme['top_frame'], fg=self.theme['fg']).pack(pady=5)
        tk.Label(self.task_win, text=f"Priorité: {infos[3]}", bg=self.theme['top_frame'], fg=self.theme['fg']).pack(pady=5)

    def close_task_window(self):
        self.task_win.destroy()