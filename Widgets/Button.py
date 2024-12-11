# -- Imports -- #
import tkinter as tk
from typing import Tuple, Optional, Callable

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

class Button:
    def __init__(self, parent, text:str = 'Button', font:Tuple = ('San Francisco', 10),
                 width:int = 100, height: int = 30, radius: int = 15, 
                 color:str = '#2B593F', hover_color:str = '#23312A', active_color:str = '#1E2A23',
                 fg:str = '#FFFFFF', bg:str = '', command:Optional[Callable] = None):
        
        # -- Initialization -- #
        self.parent = parent
        self.text = text
        self.font = font
        self.width = width
        self.height = height
        self.r = radius
        self.color = color
        self.hover_color = hover_color
        self.active_color = active_color
        self.fg = fg
        self.bg = bg or self._get_parent_bg()
        self.command = command

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        # -- Functions call -- #
        self._draw()
        self._binds()

    # -- Drawing Elements -- #
    def _draw(self):
        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, self.r, fill=self.color, tags='btn_rect')
        self.c.create_text(self.width//2, self.height//2, text=self.text, fill=self.fg, font=self.font, anchor='center', tags='btn_text')
        self.c.create_rectangle(0, 0, self.width, self.height, fill='', outline='', tags='hitbox')

    # -- Event Bindings -- #
    def _binds(self):
        self.c.tag_bind('hitbox', '<Enter>', lambda e: self._btn_hover('enter'))
        self.c.tag_bind('hitbox', '<Leave>', lambda e: self._btn_hover('leave'))
        self.c.tag_bind('hitbox', '<Button-1>', lambda e: self._btn_click('click'))
        self.c.tag_bind('hitbox', '<ButtonRelease-1>', lambda e: self._btn_click('release'))

    # -- Event Handlers -- #
    def _btn_click(self, state: str):
        if state == 'release' and self.command:
            self.command()
            try:
                self.c.itemconfig('btn_rect', fill=self.hover_color)
            except:
                pass
        elif state == 'click' and self.command:
            self.c.itemconfig('btn_rect', fill=self.active_color)

    def _btn_hover(self, state: str):        
        if state == 'enter':
            fill_color = self.hover_color 
        else: 
            fill_color = self.color
        self.c.itemconfig('btn_rect', fill=fill_color)

    # -- Utility Methods -- #
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