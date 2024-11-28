import tkinter as tk
import platform
from datetime import datetime
import widgets
from theme_loader import ThemeManager
from task_manager import TaskManager

# -- For the black title bar -- #
if platform.system() == 'Windows':
    from hPyT import *

class App(tk.Tk):
    def __init__(self, *arg, **kwargs):
        tk.Tk.__init__(self, *arg, **kwargs)
        self.title('Task·Me')
        self.geometry("1000x600")
        
        self.task_manager = TaskManager()
        self.theme_manager = ThemeManager()
        self.apply_theme()

        self.main_page()

    def apply_theme(self):
        self.theme = self.theme_manager.get_current_theme()
        self.configure(bg=self.theme['background'])
        if platform.system() == 'Windows':
            title_bar_color.set(self, self.theme['title_bar'])

    def main_page(self):
        # -- Top Section -- #
        top_frame = tk.Frame(self, bg=self.theme['top_frame'], width=1000, height=50)
        top_frame.pack(side='top')

        # -- Bottom Section -- #
        bottom_frame = tk.Frame(self, width=1000, height=550)
        bottom_frame.pack(side='bottom', fill='both', expand=True)

        # -- Left Frame -- #
        left_frame = tk.Frame(bottom_frame, bg=self.theme['left_frame'], width=200)
        left_frame.pack(side='left', fill='y')
        
        # -- Main Frame -- #
        main_frame = tk.Frame(bottom_frame, bg=self.theme['main_frame'])
        main_frame.pack(side='right', fill='both', expand=True)

        # -- Tasks Frames -- #
        today_frame = tk.Frame(main_frame, bg=self.theme['main_frame'])
        today_frame.pack(fill='x', padx=10, pady=(10, 5))
        later_frame = tk.Frame(main_frame, bg=self.theme['main_frame'])
        later_frame.pack(fill='x', padx=10, pady=(5, 10))

        tk.Label(today_frame, text="Today", font=('San Francisco', 14, 'bold'), bg=self.theme['main_frame'], fg=self.theme['fg']).pack(anchor='w')
        tk.Label(later_frame, text="Later", font=('San Francisco', 14, 'bold'), bg=self.theme['main_frame'], fg=self.theme['fg']).pack(anchor='w')

        # -- Tasks Widgets -- #
        tasks = self.task_manager.get_tasks()
        today = datetime.now().date()

        widget_width = 200 
        padding = 20
        available_width = main_frame.winfo_width() - padding
        num_columns = max(1, available_width // (widget_width + padding))

        today_tasks = [task for task in tasks if datetime.strptime(task['date'], '%Y-%m-%d').date() == today]
        later_tasks = [task for task in tasks if datetime.strptime(task['date'], '%Y-%m-%d').date() > today]

        self.create_task_grid(today_frame, today_tasks)
        self.create_task_grid(later_frame, later_tasks)

        theme_button = widgets.Button(left_frame, text="New task", color=self.theme['button'], hover_color=self.theme['hover_button'], fg=self.theme['fg'], width=180, command=self.add_task_window)
        theme_button.place(x=10, y=50)

        # -- Theme Switcher -- #
        theme_button = widgets.Button(left_frame, text="Switch Theme", color=self.theme['button'], hover_color=self.theme['hover_button'], fg=self.theme['fg'], width=180, command=self.switch_theme)
        theme_button.place(x=10, y=10)

        entry = widgets.Entry(left_frame, color=self.theme['entry'], border_color=self.theme['entry_border'], fg=self.theme['fg'], width=180)
        entry.place(x=10, y=90)

    def create_task_grid(self, parent_frame, tasks):
        tasks_per_row = 3 
        for i, task in enumerate(tasks):
            if i % tasks_per_row == 0:
                row_frame = tk.Frame(parent_frame, bg=self.theme['main_frame'])
                row_frame.pack(fill='x', expand=True)

            w = widgets.TaskWidget(row_frame, 
                                text=task['text'], 
                                date=task['date'], 
                                hour=task['hour'], 
                                priority=task['priority'],
                                bg=self.theme['main_frame'])
            w.pack(side='left', padx=10, pady=10)

    def add_task_window(self):

        newtaskWindow = tk.Tk()
        width, height = 250, 250
        posx, posy = ( self.winfo_x() + self.winfo_width()//2 ) - width // 2, ( self.winfo_y() + self.winfo_height()//2 ) - height // 2

        newtaskWindow.title('Add·Task')
        newtaskWindow.geometry(f'{width}x{height}+{posx}+{posy}')
        newtaskWindow.resizable(False, False)
        newtaskWindow.configure(bg=self.theme['top_frame'])

        if platform.system() == 'Windows':
            title_bar_color.set(newtaskWindow, self.theme['title_bar'])
            minimize_button.disable(newtaskWindow)
        
        entry1 = widgets.Entry(newtaskWindow, placeholder_text='Name', color=self.theme['entry'], border_color=self.theme['entry_border'], fg=self.theme['fg'], width=230)
        entry1.place(x=10, y=10)

        newtaskWindow.mainloop()

    def switch_theme(self):
        current_theme = self.theme_manager.current_theme_name
        new_theme = "Default Light" if current_theme == "Default Dark" else "Default Dark"
        self.theme_manager.set(new_theme)
        self.apply_theme()
        self.recreate_widgets()

    def recreate_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.main_page()

if __name__ == "__main__":
    app = App()
    app.mainloop()