# -- Imports -- #
import tkinter as tk

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

class Switch:
    def __init__(self, parent, width:int=60, height:int=32, radius:int=32, state:bool=False,
                 color:str='#2B2F31', border_color:str='#35393B', active_color:str='#049D56', active_border_color:str='#038F4D', bg=''):

        # -- Initialization -- #       
        self.parent = parent
        self.width = width
        self.height = height
        self.r = radius
        self.state = state
        self.color = color
        self.border_color = border_color
        self.active_color = active_color
        self.active_border_color = active_border_color
        self.bg = bg or self._get_parent_bg()
        self.circle_color = self.bg

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)

        self._draw()
        self._binds()

    def _draw(self):
        if self.state == False:
            create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.border_color, tags='border')
            create_rounded_rectangle(self.c, 1, 1, self.width-1, self.height-1, radius=self.r, fill=self.color, tags='rect')
            self.c.create_oval(2, 2, self.height-3, self.height-3, fill=self.bg, width=0, tags='round')
        elif self.state == True:
            create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.active_border_color, tags='border')
            create_rounded_rectangle(self.c, 1, 1, self.width-2, self.height-2, radius=self.r-4, fill=self.active_color, tags='rect')
            self.c.create_oval(self.width-2, 2, self.width-(self.height-3), self.height-3, fill=self.bg, width=0, tags='round')
        self.c.create_rectangle(0, 0, self.width, self.height, fill='', outline='', tags='hitbox')

    def _binds(self):
        self.c.tag_bind('hitbox', '<Button-1>', lambda e: self._switch_click())

    def _switch_click(self):
        self.state = not self.state
        self.c.delete('all')
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