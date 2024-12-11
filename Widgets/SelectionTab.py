# -- Imports -- #
import tkinter as tk
from typing import Tuple, Callable

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

class SelectionTab:
    def __init__(self, parent, tabs_name:list[str], tabs_command:list[Callable], width=100, tab_height=50, radius:int = 15, font:Tuple[str, int] = ('San Francisco', 10, 'bold'), 
                 bg:str = '', fg:str = '#FFFFFF', color:str = '', hover_color:str = '#343434', active_color:str = '#222222', separator_color:str ='#555555'):

        # -- Initialization -- #
        self.parent = parent
        self.tabs_name = tabs_name
        self.tabs_command = tabs_command
        self.tab_height = tab_height
        self.width = width
        self.height = tab_height * len(self.tabs_name)
        self.r = radius
        self.font = font
        self.bg = bg or self._get_parent_bg()
        self.fg = fg
        self.color = color or self.bg
        self.hover_color = hover_color
        self.active_color = active_color
        self.separator_color = separator_color

        if len(self.tabs_name) != len(self.tabs_command):
            raise ValueError("Le nombre de noms d'onglets doit correspondre au nombre de commandes d'onglets.")

        # -- Canvas Creation -- #
        self.f = tk.Frame(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        self._draw()
        

    def _draw(self):
        for i in range(len(self.tabs_name)):
            c = tk.Canvas(self.f, width=self.width, height=self.tab_height, bg=self.bg, highlightthickness=0)
            c.place(x=0, y=self.tab_height*i)

            create_rounded_rectangle(c, 0, 0, self.width, self.tab_height, radius=self.r, fill=self.color, tags='tab_rect')
            c.create_text(self.width//2, self.tab_height//2, text=self.tabs_name[i], font=self.font, fill=self.fg, anchor='center')
            c.create_rectangle(0, 0, self.width, self.tab_height, fill='', outline='', tags='hitbox')

            self._binds(c, i)

            if i > 0 :
                c.create_line(0+10, 0, self.width-10, 0, width=2, fill=self.separator_color)

    def _binds(self, tab_canvas, i):
        tab_canvas.tag_bind('hitbox', '<Enter>', lambda e, tab=tab_canvas: self._tab_hover(tab, 'enter'))
        tab_canvas.tag_bind('hitbox', '<Leave>', lambda e, tab=tab_canvas: self._tab_hover(tab, 'leave'))
        tab_canvas.tag_bind('hitbox', '<Button-1>', lambda e, tab=tab_canvas, index=i: self._tab_click('click', tab, index))
        tab_canvas.tag_bind('hitbox', '<ButtonRelease-1>', lambda e, tab=tab_canvas, index=i: self._tab_click('release', tab, index))

    def _tab_hover(self, canvas, state): 
        if state == 'enter' :
            fill_color = self.hover_color
        else:
            fill_color = self.color
        canvas.itemconfig('tab_rect', fill=fill_color)

    def _tab_click(self, state, canvas, i):
        if state == 'release':
            self.tabs_command[i]()
            canvas.itemconfig('tab_rect', fill=self.hover_color)
        elif state == 'click':
            canvas.itemconfig('tab_rect', fill=self.active_color)

    def _get_parent_bg(self):
        window_color = self.parent.cget('bg')
        rgb_values = self.parent.winfo_rgb(window_color)
        return '#{:02x}{:02x}{:02x}'.format(rgb_values[0] // 256, rgb_values[1] // 256, rgb_values[2] // 256)

    # -- Layout Methods -- #
    def pack(self, **kwargs):
        self.f.pack(**kwargs)
    def pack_forget(self, **kwargs):
        self.f.pack_forget(**kwargs)

    def place(self, **kwargs):
        self.f.place(**kwargs)
    def place_forget(self, **kwargs):
        self.f.place_forget(**kwargs)

    def grid(self, **kwargs):
        self.f.grid(**kwargs)
    def grid_forget(self, **kwargs):
        self.f.grid_forget(**kwargs)