import tkinter as tk
import platform
if platform.system() == 'Windows':
    from hPyT import *
import Widgets as widgets
from Managers.themeManager import *

class SettingsPage:
    def __init__(self, parent, theme, page_manager):
        self.parent = parent
        self.theme = theme
        self.page_manager = page_manager
        self.frame = tk.Frame(parent)

        self.theme_manager = ThemeManager()
        self.theme_names = self.theme_manager.load_themes_names()

        self.title_font = ('San Francisco', 10, 'bold')

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

        tab_selection = widgets.SelectionTab(self.left_frame, hover_color=self.theme['hover_tab_selection'], active_color=self.theme['active_tab_selection'], separator_color=self.theme['separator_tab_selection'], fg=self.theme['fg'], width=190, tabs_name=['General', 'Appearance'], tabs_command=[lambda: self.tabs_commands('General'), lambda: self.tabs_commands('Appearance')])
        tab_selection.place(x=10, y=10)

        btn = widgets.Button(self.left_frame, text='Save', color=self.theme['green_button'], hover_color=self.theme['hover_green_button'], active_color=self.theme['active_green_button'], width=190, font=('San Francisco', 10, 'bold'), command=self.save_settings)
        btn.place(x=10, y=510)

        self.tabs_commands('General')

    def home_command(self):
        self.page_manager.change_page('mainPage')

    def settings_command(self):
        self.page_manager.change_page('settingsPage')

    def tabs_commands(self, tab):
        self.current_tab = tab
        self.load_tab(tab)

    def load_tab(self, tab):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if tab == 'General':
            self.load_general_settings()
        elif tab == 'Appearance':
            self.load_appearance_settings()

    def load_general_settings(self):
        language_label = tk.Label(self.main_frame, text="Language:", font=self.title_font, bg=self.theme['main_frame'], fg=self.theme['fg'])
        language_label.pack(anchor='w', padx=10, pady=(20, 5))

        language_options = ['English', 'Français', 'Español']
        language_menu = widgets.MenuButton(self.main_frame, options=language_options, color=self.theme["menu_button"], hover_color=self.theme["hover_menu_button"], fg=self.theme['fg'], option_color=self.theme['menu_button_option'], width=200)
        language_menu.pack(anchor='w', padx=10, pady=5)

        notifications_label = tk.Label(self.main_frame, text="Enable Notifications:", font=self.title_font, bg=self.theme['main_frame'], fg=self.theme['fg'])
        notifications_label.pack(anchor='w', padx=10, pady=(20, 5))  

        self.notifications_var = tk.BooleanVar()
        switch = widgets.Switch(self.main_frame, state=True)
        switch.pack(anchor='w', padx=10)

    def load_appearance_settings(self):
        theme_label = tk.Label(self.main_frame, text="Theme:", font=self.title_font, bg=self.theme['main_frame'], fg=self.theme['fg'])
        theme_label.pack(anchor='w', padx=10, pady=(20, 5))

        theme_menu = widgets.MenuButton(self.main_frame, options=self.theme_names, color=self.theme["menu_button"], hover_color=self.theme["hover_menu_button"], fg=self.theme['fg'], option_color=self.theme['menu_button_option'], width=200)
        theme_menu.pack(anchor='w', padx=10, pady=5) 

        font_size_label = tk.Label(self.main_frame, text="Font Size:", font=self.title_font, bg=self.theme['main_frame'], fg=self.theme['fg'])
        font_size_label.pack(anchor='w', padx=10, pady=(20, 5))

        self.font_size_var = tk.IntVar(value=12)
        font_size_scale = tk.Scale(self.main_frame, from_=8, to=20, orient=tk.HORIZONTAL, variable=self.font_size_var,
                                bg=self.theme['main_frame'], fg=self.theme['fg'], highlightthickness=0)
        font_size_scale.pack(anchor='w', padx=10)

    def save_settings(self):
        pass