import tkinter as tk

class Slider:
    def __init__(self, parent, width:int=150, height:int=30, start:int=10, end:int=20, 
                 color:str='#049D56', line_color:str='#313131', bg:str='', ticks:int=10):
    
        # -- Initialization -- #
        self.parent = parent
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.color = color
        self.line_color = line_color
        self.bg = bg or self._get_parent_bg()
        self.ticks = ticks  # Nombre de crans

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, 
                           bg=self.bg, highlightthickness=0)

        # -- Slider specific variables -- #
        self.value = start
        self.slider_radius = 10
        self.slider = None
        self.colored_line = None
        self.background_line = None

        # -- Functions call -- #
        self._draw()
        self._binds()

    def _draw(self):
        self.c.create_oval(self.height//2-4, self.height//2-4, self.height//2+4, self.height//2+4, fill=self.color, width=0)
        self.c.create_oval(self.width-self.height//2-4, self.height//2-4, self.width-self.height//2+4, self.height//2+4, fill=self.line_color, width=0)

        self.background_line = self.c.create_line(
            self.height//2, self.height//2, 
            self.width-self.height//2, self.height//2, 
            width=9, fill=self.line_color
        )

        self.colored_line = self.c.create_line(
            self.height//2, self.height//2, 
            self.height//2, self.height//2,
            width=9, fill=self.color
        )

        x = self._value_to_x()
        self.slider = self.c.create_oval(
            x-self.slider_radius, self.height//2-self.slider_radius, 
            x+self.slider_radius, self.height//2+self.slider_radius, 
            fill=self.color, outline=self.color
        )

    def _binds(self):
        self.c.bind("<Button-1>", self._on_click)
        self.c.bind("<B1-Motion>", self._on_drag)

    def _on_click(self, event):
        self._update_slider(event.x)

    def _on_drag(self, event):
        self._update_slider(event.x)

    def _update_slider(self, x):
        x = max(self.height//2, min(x, self.width - self.height//2))

        tick_spacing = (self.width - self.height) / (self.ticks - 1)
        nearest_tick = round((x - self.height // 2) / tick_spacing) * tick_spacing + self.height // 2
        self.value = self._x_to_value(nearest_tick)

        self.c.coords(self.slider, 
            nearest_tick - self.slider_radius, self.height//2 - self.slider_radius, 
            nearest_tick + self.slider_radius, self.height//2 + self.slider_radius
        )
        self.c.coords(self.colored_line,
            self.height//2, self.height//2, nearest_tick, self.height//2
        )

    def _value_to_x(self):
        return int((self.value - self.start) / (self.end - self.start) * 
                   (self.width - self.height) + self.height//2)

    def _x_to_value(self, x):
        return int((x - self.height//2) / (self.width - self.height) * 
                   (self.end - self.start) + self.start)

    def _get_parent_bg(self):
        window_color = self.parent.cget('bg')
        rgb_values = self.parent.winfo_rgb(window_color)
        return '#{:02x}{:02x}{:02x}'.format(
            rgb_values[0] // 256, 
            rgb_values[1] // 256, 
            rgb_values[2] // 256
        )
    
    def get(self):
        return self.value

    def set(self, value):
        self.value = max(self.start, min(value, self.end))
        x = self._value_to_x()
        self.c.coords(self.slider, 
            x-self.slider_radius, self.height//2-self.slider_radius, 
            x+self.slider_radius, self.height//2+self.slider_radius
        )
        self.c.coords(self.colored_line,
            self.height//2, self.height//2, x, self.height//2
        )

    # Méthodes de layout standard
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