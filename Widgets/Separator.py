# -- Imports -- #
import tkinter as tk
from typing import Tuple, Callable

class Separator:
    def __init__(self, parent, thickness:int=1, color:str='#444444', bg:str=''):

        self.parent = parent
        self.thickness = thickness
        self.color = color
        self.bg = bg or self._get_parent_bg()

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, height=self.thickness, bg=self.bg, highlightthickness=0)

        self._draw()

        self.c.bind("<Configure>", self._on_configure)


    def _draw(self):
        self.c.delete("all")
        width = self.c.winfo_width()
        height = self.c.winfo_height()
        self.c.create_line(10, height//2, width-10, height//2, fill=self.color)

    def _on_configure(self, event):
        self._draw()

    def _get_parent_bg(self):
        window_color = self.parent.cget('bg')
        rgb_values = self.parent.winfo_rgb(window_color)
        return '#{:02x}{:02x}{:02x}'.format(rgb_values[0] // 256, rgb_values[1] // 256, rgb_values[2] // 256)

    # -- Layout Methods -- #
    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    def pack_forget(self, **kwargs):
        self.c.pack_forget(**kwargs)

    def place(self, **kwargs):
        self.c.place(**kwargs)
    def place_forget(self, **kwargs):
        self.c.place_forget(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)
    def grid_forget(self, **kwargs):
        self.c.grid_forget(**kwargs)