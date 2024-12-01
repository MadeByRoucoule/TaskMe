import tkinter as tk
import platform
if platform.system() == 'Windows':
    from hPyT import *
import widgets

class SettingsPage:
    def __init__(self, parent, theme, page_manager):
        self.parent = parent
        self.theme = theme
        self.page_manager = page_manager
        self.frame = tk.Frame(parent)
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

        home_btn = widgets.Button(self.top_frame, text='Home', color=self.theme['button'], hover_color=self.theme['hover_button'], active_color=self.theme['active_button'], width=100, font=('San Francisco', 10, 'bold'), command=self.home_command)
        home_btn.place(x=10, y=10)
        settings_btn = widgets.Button(self.top_frame, text='Settings', color=self.theme['button'], hover_color=self.theme['hover_button'], active_color=self.theme['active_button'], width=100, font=('San Francisco', 10, 'bold'), command=self.settings_command)
        settings_btn.place(x=120, y=10)

    def home_command(self):
        self.page_manager.change_page('mainPage')

    def settings_command(self):
        self.page_manager.change_page('settingsPage')