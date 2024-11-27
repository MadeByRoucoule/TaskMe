import tkinter as tk
import platform
from widget import TaskWidget

# -- For the black title bar -- #
if platform.system()=='Windows':
    from hPyT import *

class App(tk.Tk):
    def __init__(self, *arg, **kwargs):
        tk.Tk.__init__(self, *arg, **kwargs)
        self.title('TaskMe')
        self.geometry("1000x600")
        self.configure(bg='#1B1B1B')

        if platform.system()=='Windows':
            title_bar_color.set(self, '#2B2B2B')

        self.main_page()

    def main_page(self):

        # -- Top Section -- #

        top_frame = tk.Frame(self, bg='#2B2B2B', width=1000, height=50)
        top_frame.grid(row=0, column=0, columnspan=2)

        # -- Main Section -- #

        main_frame = tk.Frame(self, bg='#1B1B1B')
        main_frame.grid(row=1, column=0)

        w = TaskWidget(main_frame)
        w.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    print(platform.system())