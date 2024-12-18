import tkinter as tk
from datetime import datetime
import platform
if platform.system() == 'Windows':
    from hPyT import *
import Widgets as widgets
import Managers as manager

class MainPage:
    def __init__(self, parent, theme, page_manager):
        
        self.parent = parent
        self.theme = theme
        self.page_manager = page_manager
        self.task_manager = manager.TasksManager()
        self.notif_manager = manager.NotificationManager()
        self.notif_manager.start()
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

        sorted_menubutton = widgets.MultipleMenuButton(self.top_frame, text='Sorted by', color=self.theme["top_menu_button"], hover_color=self.theme["hover_menu_button"], fg=self.theme['fg'], option_color=self.theme['menu_button_option'], options=['Time', 'Priority'], width=150, command=self.update_sort_options)
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
        try:
            tasks = self.task_manager.get_sorted_tasks(tab, self.current_sort_options)
        except Exception as e:
            tasks = []

        y = 10
        x = 10
        tasks_per_row = 3

        for task in tasks:
            w = widgets.TaskWidget(
                self.main_frame,
                radius=25,
                text=task['text'],
                date=task.get('date', ''),
                hour=task.get('hour', ''),
                priority=task.get('priority', 'Low'),
                completed=True,
                fg=self.theme['fg'],
                priority_colors=self.theme['priority_colors'],
                hover_priority_colors=self.theme['hover_priority_colors'],
                width=250,
                tag=task['text'],
                command=lambda t=task['text']: self.open_task_window(t)
            )
            w.place(x=x, y=y)
            tasks_per_row -= 1
            if tasks_per_row == 0:
                y += 110
                x = 10
                tasks_per_row = 3
            else:
                x += 260

            self.add_notification_for_task(task)

    def add_notification_for_task(self, task):
        try:
            task_date = task.get('date')
            task_time = task.get('hour')
            if not task_date or not task_time:
                return

            formatted_datetime = f"{task_date} {task_time.replace('h', ':')}"
            notification_datetime = datetime.strptime(formatted_datetime, "%d/%m/%Y %H:%M")

            if (notification_datetime > datetime.now()) and (task['text'] not in [n['title'] for n in self.notif_manager.notifications]):
                self.notif_manager.add_notification(
                    title=task['text'],
                    message=task['note'] if task['note'] else "Pas de note disponible",
                    date_time=notification_datetime
                )
        except Exception as e:
            pass

    def update_sort_options(self, selected_options):
        for option in ['Time', 'Priority']:
            if option in selected_options and option not in self.current_sort_options:
                self.current_sort_options.append(option)
            elif option not in selected_options and option in self.current_sort_options:
                self.current_sort_options.remove(option)
        self.update_tasks_widgets()

    def is_today(self, date_str):
        if not date_str:
            return False
        try:
            today = datetime.date.today()
            task_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
            return task_date == today
        except ValueError: 
            return False
        
    def is_future(self, date_str):
        if not date_str:
            return False
        try:
            today = datetime.date.today()
            task_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
            return task_date > today
        except ValueError:
            return False
    
    def is_before(self, date_str):
        if not date_str:
            return False
        try:
            today = datetime.date.today()
            task_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
            return task_date < today
        except ValueError:
            return False

    def open_task_window(self, tag):
        taskWindow = TaskWindow(self.parent, self.theme, tag,  self)
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

        task_manager = manager.TasksManager()
        if self.name_entry.get() != '' and self.date_entry.get() and self.hour_entry.get()!= '' and self.priority_btn.selected_option != None :
            task_manager.add_task(self.name_entry.get(), self.date_entry.get(), self.hour_entry.get(), self.priority_btn.selected_option)
            self.update_tasks_widgets()
            self.add_task_win.destroy()
        else :
            print('Error : please enter informations')

class TaskWindow():
    def __init__(self, parent, theme, tag, main_page):
        self.parent = parent
        self.theme = theme
        self.main_page = main_page
        self.task_manager = manager.TasksManager()
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

        self.task_win.bind("<FocusOut>", lambda e: self.on_focus_out(e))

        bottom_frame = tk.Frame(self.task_win, bg=self.theme['top_frame'])
        bottom_frame.pack(side='bottom', fill='x')

        tk.Label(self.task_win, text=self.infos[0], font=('San Francisco', 16, 'bold'), bg=self.theme['top_frame'], fg=self.theme['fg']).pack(pady=10)
        
        separator = widgets.Separator(self.task_win, color=self.theme['2ndseparator'])
        separator.pack()

        info_frame = tk.Frame(self.task_win, bg=self.theme['top_frame'])
        info_frame.pack(pady=20, padx=10, fill='x')
        tk.Label(info_frame, text=f"Date: {self.infos[1]}", font=('San Francisco', 10), bg=self.theme['top_frame'], fg=self.theme['fg']).pack(padx=10, pady=5, anchor='w')
        tk.Label(info_frame, text=f"Heure: {self.infos[2]}", font=('San Francisco', 10), bg=self.theme['top_frame'], fg=self.theme['fg']).pack(padx=10, pady=5, anchor='w')
        tk.Label(info_frame, text=f"Priorité: {self.infos[3]}", font=('San Francisco', 10), bg=self.theme['top_frame'], fg=self.theme['fg']).pack(padx=10, pady=5, anchor='w')

        separator = widgets.Separator(info_frame, color=self.theme['2ndseparator'])
        separator.pack(pady=20)

        self.note_area = widgets.TextArea(info_frame, height=200, color=self.theme["entry"], border_color=self.theme['entry_border'], fg=self.theme['fg'])
        self.note_area.pack(padx=10, pady=5, fill='x')
        self.note_area.insert(tk.END, str(self.infos[4]))

        separator = widgets.Separator(self.task_win, color=self.theme['2ndseparator'])
        separator.pack()

        delete_btn = widgets.Button(bottom_frame, text='Delete', color=self.theme['red_button'], hover_color=self.theme['hover_red_button'], active_color=self.theme['active_red_button'], width=150, command=self.delete)
        delete_btn.pack(side='left', padx=10, pady=10)
        done_btn = widgets.Button(bottom_frame, text='Save', color=self.theme['green_button'], hover_color=self.theme['hover_green_button'], active_color=self.theme['active_green_button'], width=150, command=self.save)
        done_btn.pack(side='right', padx=10, pady=10)

    def on_focus_out(self, event):
        if not self.task_win.focus_displayof():
            self.close_task_window()
    
    def close_task_window(self):
        self.task_win.destroy()

    def save(self):
        updated_task = {
            "text": self.infos[0],  
            "date": self.infos[1],  
            "hour": self.infos[2],  
            "priority": self.infos[3],  
            "note": self.note_area.get()
        }

        tasks = self.task_manager.load_tasks()

        for task in tasks['tasks']:
            if task['text'] == updated_task['text']:
                task.update(updated_task) 
                break
        
        self.task_manager.save_task(tasks)
        self.close_task_window()

    def delete(self):
        self.task_manager.delete_task(self.infos[0])
        self.main_page.update_tasks_widgets()
        self.close_task_window()