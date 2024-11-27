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
        top_frame.pack(side='top')

        # -- Bottom Section -- #

        bottom_frame = tk.Frame(self, width=1000, height=550)
        bottom_frame.pack(side='bottom', fill='both', expand=True)

        # -- Left Frame -- #

        left_frame = tk.Frame(bottom_frame, bg='#222222', width=200)
        left_frame.pack(side='left', fill='y')
        
        # -- Main Frame -- #

        main_frame = tk.Frame(bottom_frame, bg='#1B1B1B')
        main_frame.pack(side='right', fill='both', expand=True)

        w = TaskWidget(main_frame)
        w.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    print(platform.system())