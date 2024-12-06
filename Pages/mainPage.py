import tkinter as tk
import datetime
import platform
if platform.system() == 'Windows':
    from hPyT import *
import widgets
from Managers.tasksManager import TasksManager

class MainPage:
    def __init__(self, parent, theme, page_manager):
        
        self.parent = parent
        self.theme = theme
        self.page_manager = page_manager
        self.frame = tk.Frame(parent)

        self.current_tab = 'All'
        self.current_sort_options = []
        
        self.frames()
        self.widgets()

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

    def frames(self):

        # -- Top Section -- #
        self.top_frame = tk.Frame(self.frame, bg=self.theme['top_frame'], width=1000, height=50)
        self.top_frame.pack(side='top')

        # -- Bottom Section -- #
        self.bottom_frame = tk.Frame(self.frame, width=1000, height=550)
        self.bottom_frame.pack(side='bottom', fill='both', expand=True)

        # -- Left Frame -- #
        self.left_frame = tk.Frame(self.bottom_frame, bg=self.theme['left_frame'], width=210)
        self.left_frame.pack(side='left', fill='y')
        
        # -- Main Frame -- #
        self.main_frame = tk.Frame(self.bottom_frame, bg=self.theme['main_frame'])
        self.main_frame.pack(side='right', fill='both', expand=True)

    def widgets(self):

        home_btn = widgets.Button(self.top_frame, text='Home', color=self.theme['button'], hover_color=self.theme['hover_button'], active_color=self.theme['active_button'], fg=self.theme['fg'], width=100, font=('San Francisco', 10, 'bold'), command=self.home_command)
        home_btn.place(x=10, y=10)
        settings_btn = widgets.Button(self.top_frame, text='Settings', color=self.theme['button'], hover_color=self.theme['hover_button'], active_color=self.theme['active_button'], fg=self.theme['fg'], width=100, font=('San Francisco', 10, 'bold'), command=self.settings_command)
        settings_btn.place(x=120, y=10)

        sorted_menubutton = widgets.MultipleMenuButton(self.top_frame, text='Sorted by', color=self.theme["menu_button"], hover_color=self.theme["hover_menu_button"], fg=self.theme['fg'], option_color=self.theme['menu_button_option'], options=['Time', 'Priority'], width=150, command=self.update_sort_options)
        sorted_menubutton.place(x=840, y=10)

        tab_selection = widgets.SelectionTab(self.left_frame, hover_color=self.theme['hover_tab_selection'], active_color=self.theme['active_tab_selection'], separator_color=self.theme['separator_tab_selection'], fg=self.theme['fg'], width=190, tabs_name=['All', 'Today', 'Later', 'Before'], tabs_command=[lambda: self.tabs_commands('All'), lambda: self.tabs_commands('Today'), lambda: self.tabs_commands('Later'), lambda: self.tabs_commands('Before')])
        tab_selection.place(x=10, y=10)

        btn = widgets.Button(self.left_frame, text='Add Task', color=self.theme['green_button'], hover_color=self.theme['hover_green_button'], active_color=self.theme['active_green_button'], width=190, font=('San Francisco', 10, 'bold'), command=self.add_task)
        btn.place(x=10, y=510)

        self.update_tasks_widgets()

    def tabs_commands(self, tab):
        self.current_tab = tab
        self.update_tasks_widgets()

    def home_command(self):
        self.page_manager.change_page('mainPage')

    def settings_command(self):
        self.page_manager.change_page('settingsPage')

    def update_tasks_widgets(self, tab=None):
        if tab is None:
            tab = self.current_tab
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        task_manager = TasksManager()
        tasks = task_manager.load_tasks()['tasks']

        if tab == 'Today':
            tasks = [task for task in tasks if self.is_today(task.get('date', ''))]
        elif tab == 'Later':
            tasks = [task for task in tasks if self.is_future(task.get('date', ''))]
        elif tab == 'Before':
            tasks = [task for task in tasks if self.is_before(task.get('date', ''))]

        if 'Time' in self.current_sort_options:
            tasks.sort(key=lambda x: (x.get('date', ''), x.get('hour', '')))
        
        if 'Priority' in self.current_sort_options:
            priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
            tasks.sort(key=lambda x: priority_order.get(x.get('priority', 'Low'), 3))

        y = 10
        x = 10
        tasks_per_row = 3

        for task in tasks:
            w = widgets.TaskWidget(self.main_frame, radius=25, text=task['text'], 
                                date=task.get('date', ''), hour=task.get('hour', ''), 
                                priority=task.get('priority', 'Low'), completed=True, 
                                fg=self.theme['fg'], 
                                priority_colors=self.theme['priority_colors'], 
                                hover_priority_colors=self.theme['hover_priority_colors'], 
                                width=250, tag=task['text'], 
                                command=lambda t=task['text']: self.open_task_window(t))
            w.place(x=x, y=y)
            tasks_per_row -= 1
            if tasks_per_row == 0:
                y += 100 + 10
                x = 10
                tasks_per_row = 3
            else:
                x += 250 + 10

    def is_today(self, date_str):
        if not date_str:
            return False
        try:
            today = datetime.date.today()
            task_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
            return task_date == today
        except ValueError: 
            print(f"Date invalide: {date_str}")
            return False
        
    def is_future(self, date_str):
        if not date_str:
            return False
        try:
            today = datetime.date.today()
            task_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
            return task_date > today
        except ValueError:
            print(f"Date invalide: {date_str}")
            return False
    
    def is_before(self, date_str):
        if not date_str:
            return False
        try:
            today = datetime.date.today()
            task_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
            return task_date < today
        except ValueError:
            print(f"Date invalide: {date_str}")
            return False

    def update_sort_options(self, selected_options):
        self.current_sort_options = selected_options
        self.update_tasks_widgets()

    def open_task_window(self, tag):
        taskWindow = TaskWindow(self.parent, self.theme, tag)
        self.update_tasks_widgets(self.current_tab)

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
        self.priority_btn = widgets.MenuButton(self.add_task_win, options=priority, color=self.theme["menu_button"], hover_color=self.theme["hover_menu_button"], fg=self.theme['fg'], option_color=self.theme['menu_button_option'], width=200)
        self.priority_btn.pack(pady=5)

        self.cancel_btn = widgets.Button(self.add_task_win, text='Cancel', color=self.theme['red_button'], hover_color=self.theme['hover_red_button'], active_color=self.theme['active_red_button'], width=200,command=lambda: self.add_task_win.destroy())
        self.cancel_btn.pack(side='bottom', pady=(5,10))
        self.done_btn = widgets.Button(self.add_task_win, text='Done', color=self.theme['green_button'], hover_color=self.theme['hover_green_button'], active_color=self.theme['active_green_button'], width=200,command=self.add_task_done)
        self.done_btn.pack(side='bottom', pady=5)

    def add_task_done(self):

        task_manager = TasksManager()
        if self.name_entry.get() != '' and self.date_entry.get() and self.hour_entry.get()!= '' and self.priority_btn.selected_option != None :
            task_manager.add_task(self.name_entry.get(), self.date_entry.get(), self.hour_entry.get(), self.priority_btn.selected_option)
            self.update_tasks_widgets()
            self.add_task_win.destroy()
        else :
            print('Error : please enter informations')

class TaskWindow():
    def __init__(self, parent, theme, tag):
        self.parent = parent
        self.theme = theme
        self.task_manager = TasksManager()
        self.width, self.height = 400, 500
        self.posx, self.posy = (self.parent.winfo_x() + self.parent.winfo_width()//2) - self.width // 2, (self.parent.winfo_y() + self.parent.winfo_height()//2) - self.height // 2
        self.infos = self.task_manager.get_task_info(tag)

        self.task_win = tk.Toplevel(self.parent, bg=self.theme['top_frame'])
        self.task_win.title('Task Details')
        self.task_win.geometry(f'{self.width}x{self.height}+{self.posx}+{self.posy}')
        self.task_win.resizable(False, False)

        if platform.system() == 'Windows':
            all_stuffs.hide(self.task_win)
            title_bar_color.set(self.task_win, self.theme['title_bar'])

        self.task_win.bind("<FocusOut>", lambda e: self.close_task_window())

        bottom_frame = tk.Frame(self.task_win, bg=self.theme['top_frame'])
        bottom_frame.pack(side='bottom', fill='x')

        tk.Label(self.task_win, text=self.infos[0], font=('San Francisco', 16, 'bold'), bg=self.theme['top_frame'], fg=self.theme['fg']).pack(pady=10)
        tk.Label(self.task_win, text=f"Date: {self.infos[1]}", bg=self.theme['top_frame'], fg=self.theme['fg']).pack(pady=5)
        tk.Label(self.task_win, text=f"Heure: {self.infos[2]}", bg=self.theme['top_frame'], fg=self.theme['fg']).pack(pady=5)
        tk.Label(self.task_win, text=f"Priorité: {self.infos[3]}", bg=self.theme['top_frame'], fg=self.theme['fg']).pack(pady=5)

        delete_btn = widgets.Button(bottom_frame, text='Delete', color=self.theme['red_button'], hover_color=self.theme['hover_red_button'], active_color=self.theme['active_red_button'], width=150)
        delete_btn.pack(side='left', padx=5, pady=5)
        done_btn = widgets.Button(bottom_frame, text='Done', color=self.theme['green_button'], hover_color=self.theme['hover_green_button'], active_color=self.theme['active_green_button'], width=150)
        done_btn.pack(side='right', padx=5, pady=5)

    def close_task_window(self):
        self.task_win.destroy()