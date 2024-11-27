import tkinter as tk
from hPyT import *


class App(tk.Tk):
    def __init__(self, *arg, **kwargs):
        tk.Tk.__init__(self, *arg, **kwargs)
        self.title('TaskMe')
        self.geometry("1000x600")
        title_bar_color.set(self, '#2B2B2B')

if __name__ == "__main__":
    app = App()
    app.mainloop()
