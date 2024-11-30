import tkinter as tk
from hPyT import *
import platform
# -- Pages -- #
from Pages.mainPage import MainPage
from Managers.themeManager import ThemeManager

class App(tk.Tk):
    def __init__(self, *arg, **kwargs):
        tk.Tk.__init__(self, *arg, **kwargs)
        self.title('TaskMe')
        self.geometry("1000x600")

        self.theme_manager = ThemeManager()
        self.theme_manager.change_theme('Default Dark')
        self.apply_theme()

        MainPage(self, self.theme)

    def apply_theme(self):

        self.theme = self.theme_manager.get_current_theme()

        if platform.system() == 'Windows':
            title_bar_color.set(self, self.theme['title_bar'])

if __name__ == "__main__":
    app = App()
    app.mainloop()
