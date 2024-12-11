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

class TaskWidget:
    def __init__(self, parent, text:str, date:str, hour:str, priority:str, completed:bool,
                 width:int = 200, height:int = 100, radius:int = 15, font:Tuple = ('San Francisco', 10), 
                 color:str = '', hover_color:str = '', active_color:str = '', fg:str = '#FFFFFF', bg:str = '', 
                 priority_colors:list = ['#6E3630', '#89632A', '#2B593F'], hover_priority_colors:list = ['#3E2825', '#403324', '#23312A'], 
                 active_priority_colors:list = ["#331F1D", "#352A1E", "#1E2A23"], tag:str = '', command: Optional[Callable] = None):
        
        # -- Initialization -- #
        self.parent = parent
        self.text = text
        self.date = date
        self.hour = hour
        self.priority = priority
        self.completed = completed
        self.width = width
        self.height = height
        self.r = radius
        self.font = font
        self.title_font:Tuple = ('San Francisco', 10, 'bold')
        self.color = color
        self.hover_color = hover_color
        self.active_color = active_color
        self.fg = fg
        self.bg = bg or self._get_parent_bg()
        self.priority_color = priority_colors
        self.hover_priority_color = hover_priority_colors
        self.active_priority_colors = active_priority_colors
        self.tag = tag
        self.command = command

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        # -- Functions call -- #
        self._draw()
        self._binds()

    # -- Drawing Elements -- #
    def _draw(self):
        if not self.color and self.priority == 'High':
            create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.priority_color[0], tags='w_rect')
        elif not self.color and self.priority == 'Medium':
            create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.priority_color[1], tags='w_rect')
        elif not self.color and self.priority == 'Low':
            create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.priority_color[2], tags='w_rect')
        else:
            create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.color, tags='w_rect')
        
        self.c.create_text(15, 15, text=self.text, fill=self.fg, font=('San Francisco', 12, 'bold'), width=self.width-15*2, anchor='nw')
        self.c.create_text(10, self.height-10, text=self.date, fill=self.fg, font=self.font, anchor='sw')
        self.c.create_text(85, self.height-10, text=f'| {self.hour}', fill=self.fg, font=self.font, anchor='sw')
        self.c.create_text(self.width-10, self.height-10, text=self.priority, fill=self.fg, font=('San Francisco', 10, 'bold'), anchor='se')
        self.c.create_rectangle(0, 0, self.width, self.height, fill='', outline='', tags='hitbox')

    # -- Event Bindings -- #
    def _binds(self):
        self.c.tag_bind('hitbox', '<Enter>', lambda e: self._w_hover('enter'))
        self.c.tag_bind('hitbox', '<Leave>', lambda e: self._w_hover('leave'))
        self.c.tag_bind('hitbox', '<Button-1>', lambda e: self._w_click('click'))
        self.c.tag_bind('hitbox', '<ButtonRelease-1>', lambda e: self._w_click('release'))

    # -- Event Handlers -- #
    def _w_hover(self, state: str):        
        if state == 'enter':
            if not self.color and self.priority == 'High':
                fill_color = self.hover_priority_color[0]
            elif not self.color and self.priority == 'Medium':
                fill_color = self.hover_priority_color[1]
            elif not self.color and self.priority == 'Low':
                fill_color = self.hover_priority_color[2]
            else:
                fill_color = self.hover_color
        else: 
            if not self.color and self.priority == 'High':
                fill_color = self.priority_color[0]
            elif not self.color and self.priority == 'Medium':
                fill_color = self.priority_color[1]
            elif not self.color and self.priority == 'Low':
                fill_color = self.priority_color[2]
            else :
                fill_color = self.color
        self.c.itemconfig('w_rect', fill=fill_color)

    def _w_click(self, state):
        if state == 'release' and self.command:
            self.command(self.tag)
            if not self.color and self.priority == 'High':
                fill_color = self.hover_priority_color[0]
            elif not self.color and self.priority == 'Medium':
                fill_color = self.hover_priority_color[1]
            elif not self.color and self.priority == 'Low':
                fill_color = self.hover_priority_color[2]
            else:
                fill_color = self.hover_color
        elif state == 'click' and self.command:
            if not self.color and self.priority == 'High':
                fill_color = self.active_priority_colors[0]
            elif not self.color and self.priority == 'Medium':
                fill_color = self.active_priority_colors[1]
            elif not self.color and self.priority == 'Low':
                fill_color = self.active_priority_colors[2]
            else :
                fill_color = self.active_color
            self.c.itemconfig('w_rect', fill=fill_color)

    def get_tag(self):
        return self.tag

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