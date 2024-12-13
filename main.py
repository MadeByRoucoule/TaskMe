# -- Imports -- #
import tkinter as tk
import platform
from datetime import datetime, timedelta
if platform.system() == 'Windows':
    from hPyT import *
# -- Managers -- #
import Managers as manager

class App(tk.Tk):
    def __init__(self, *arg, **kwargs):
        tk.Tk.__init__(self, *arg, **kwargs)
        self.title('Task·Me')
        self.center_window(1000, 600)
        self.resizable(False, False)

        self.theme_manager = manager.ThemeManager()
        self.theme_manager.change_theme('Default Dark')
        self.apply_theme()

        self.notif_manager = manager.NotificationManager()
        self.notif_manager.start()

        self.notif_manager.add_notification(
            title="Notification Manager",
            message="This is the message for the notification, but I don't know the maximum width for the message in the notification.",
            date_time=datetime.now() + timedelta(seconds=5)
        )

        self.page_manager = manager.PageManager(self, self.theme)
        self.page_manager     

    def apply_theme(self):

        self.theme = self.theme_manager.get_current_theme()

        if platform.system() == 'Windows':
            title_bar_color.set(self, self.theme['title_bar'])

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    app = App()
    app.mainloop()