# -- Imports -- #
import tkinter as tk
from typing import Tuple

# -- Utility Functions -- #
def create_rounded_rectangle(canvas, x1:int, y1:int, x2:int, y2:int, radius:int, **kwargs):
    points = [x1+radius, y1,
                x1+radius, y1, x2-radius, y1,
                x2-radius, y1, x2, y1,
                x2, y1+radius, x2, y1+radius,
                x2, y2-radius, x2, y2-radius,
                x2, y2, x2-radius, y2,
                x2-radius, y2, x1+radius, y2,
                x1+radius, y2, x1, y2,
                x1, y2-radius, x1, y2-radius,
                x1, y1+radius, x1, y1+radius,
                x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)

class TextArea:
    def __init__(self, parent, font: Tuple[str, int] = ('San Francisco', 10),
                 width: int = 100, height: int = 30, radius: int = 15, border_width: int = 2,
                 color: str = '#4C4C4C', fg: str = '#FFFFFF', bg: str = '', border_color: str = '#343434'):
        
        # -- Initialization -- #
        self.parent = parent
        self.font = font
        self.font_list = tuple(font)
        self.width = width
        self.height = height
        self.r = radius
        self.border_width = border_width
        self.color = color
        self.fg = fg
        self.bg = bg or self._get_parent_bg()
        self.border_color = border_color

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        self._draw()
        self._binds()

    # -- Drawing Elements -- #
    def _draw(self):
        self.c.delete("all")

        # -- Entry Widget Creation -- #
        self.t = tk.Text(self.parent, relief=tk.FLAT, highlightthickness=0, bg=self.color, font=self.font, fg=self.fg, wrap="word")
        self.c.create_window(self.width // 2, self.height // 2, window=self.t, anchor='center', tags='entry_window', 
                             width=self.width - 15, height=self.height - 15)

        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.border_color, tags='border_rect')
        create_rounded_rectangle(self.c, self.border_width, self.border_width, self.width - self.border_width, 
                                 self.height - self.border_width, radius=self.r - self.border_width, 
                                 fill=self.color, tags='entry_rect')

    def _binds(self):
        self.c.bind("<Configure>", self._on_resize)

    # -- Event Handlers -- #
    def _on_resize(self, event):
        if event.width != self.width or event.height != self.height:
            current_text = self.get()
            self.width = event.width
            self.height = event.height
            self._draw()
            self.t.insert("1.0", current_text)

    def get(self):
        return self.t.get("1.0", tk.END).strip()

    def insert(self, index, chars, *args):
        self.t.insert(index, chars, *args)

    # -- Utility Methods -- #
    def _get_parent_bg(self):
        window_color = self.parent.cget('bg')
        rgb_values = self.parent.winfo_rgb(window_color)
        return '#{:02x}{:02x}{:02x}'.format(rgb_values[0] // 256, rgb_values[1] // 256, rgb_values[2] // 256)

    # -- Layout Methods -- #
    def pack(self, **kwargs):
        self.c.pack(**kwargs)
        if "fill" in kwargs:
            self.c.bind("<Configure>", self._on_resize)
    def pack_forget(self, **kwargs):
        self.c.pack_forget(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)
    def place_forget(self, **kwargs):
        self.c.place_forget(**kwargs)
    
    def grid(self, **kwargs):
        self.c.grid(**kwargs)
        if "fill" in kwargs:
            self.c.bind("<Configure>", self._on_resize)
    def grid_forget(self, **kwargs):
        self.c.grid_forget(**kwargs)
