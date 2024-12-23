import tkinter as tk

class Slider:
    def __init__(self, parent, width:int=150, height:int=30, start:int=0, end:int=100, text_value:bool=True, 
                 color:str='#049D56', line_color:str='#313131', bg:str='', fg:str='#ffffff', ticks:int=101, callback=None):
    
        # -- Initialization -- #
        self.parent = parent
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.text_value = text_value
        self.color = color
        self.line_color = line_color
        self.bg = bg or self._get_parent_bg()
        self.fg = fg
        self.ticks = ticks 
        self.callback = callback
        self.value = self.start

        # -- Frame Creation -- #
        self.f = tk.Frame(self.parent, width=self.width, height=self.height, 
                           bg=self.bg, highlightthickness=0)

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.f, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        self.c.pack(side='left')

        # -- Label Creation -- #
        if text_value == True:
            self.value_label = tk.Label(self.f, text=str(self.value), bg=self.bg, fg=self.fg, width=5)
            self.value_label.pack(side='right')

        # -- Slider specific variables -- #
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
        x = max(self.height // 2, min(x, self.width - self.height // 2))

        tick_spacing = (self.width - self.height) / (self.ticks - 1)
        nearest_tick_index = round((x - self.height // 2) / tick_spacing)
        self.value = self.start + nearest_tick_index * ((self.end - self.start) / (self.ticks - 1))

        x_aligned = nearest_tick_index * tick_spacing + self.height // 2
        self.c.coords(self.slider, 
            x_aligned - self.slider_radius, self.height // 2 - self.slider_radius, 
            x_aligned + self.slider_radius, self.height // 2 + self.slider_radius
        )
        self.c.coords(self.colored_line,
            self.height // 2, self.height // 2, x_aligned, self.height // 2
        )

        if self.text_value and hasattr(self, 'value_label'):
            self.value_label.config(text=str(round(self.value)))

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

    def set(self, value):
        self.value = max(self.start, min(value, self.end))
        x = self._value_to_x()
        self._update_slider(x)

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
