import tkinter as tk
import widgets

class MainPage:
    def __init__(self, parent, theme):
        
        self.parent = parent
        self.theme = theme

        self.frames()

    def frames(self):

        # -- Top Section -- #
        top_frame = tk.Frame(self.parent, bg=self.theme['top_frame'], width=1000, height=50)
        top_frame.pack(side='top')

        # -- Bottom Section -- #
        bottom_frame = tk.Frame(self.parent, width=1000, height=550)
        bottom_frame.pack(side='bottom', fill='both', expand=True)

        # -- Left Frame -- #
        left_frame = tk.Frame(bottom_frame, bg=self.theme['left_frame'], width=200)
        left_frame.pack(side='left', fill='y')
        
        # -- Main Frame -- #
        main_frame = tk.Frame(bottom_frame, bg=self.theme['main_frame'])
        main_frame.pack(side='right', fill='both', expand=True)

        btn = widgets.Button(left_frame, width=180, font=('San Francisco', 10, 'bold'))
        btn.place(x=10, y=510)
