import tkinter as tk
import platform
if platform.system() == 'Windows':
    from hPyT import *
# -- Pages -- #
from Managers.pagesManager import PageManager
from Managers.themeManager import ThemeManager

class App(tk.Tk):
    def __init__(self, *arg, **kwargs):
        tk.Tk.__init__(self, *arg, **kwargs)
        self.title('Task·Me')
        self.geometry("1000x600")
        self.resizable(False, False)

        self.theme_manager = ThemeManager()
        self.theme_manager.change_theme('Default Dark')
        self.apply_theme()

        self.page_manager = PageManager(self, self.theme)
        self.page_manager        

    def apply_theme(self):

        self.theme = self.theme_manager.get_current_theme()

        if platform.system() == 'Windows':
            title_bar_color.set(self, self.theme['title_bar'])

if __name__ == "__main__":
    app = App()
    app.mainloop()
