import tkinter as tk
import platform
from widgets import TaskWidget

# -- For the black title bar --
if platform.system()=='Windows':
    from hPyT import *

class App(tk.Tk):
    def __init__(self, *arg, **kwargs):
        tk.Tk.__init__(self, *arg, **kwargs)
        self.title('TaskMe')
        self.geometry("1000x600")
        self.configure(bg='#2B2B2B')

        if platform.system()=='Windows':
            title_bar_color.set(self, '#2B2B2B')

        w = TaskWidget(parent=self)
        w.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    print(platform.system())
