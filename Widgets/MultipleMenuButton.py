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

class MultipleMenuButton:
    def __init__(self, parent, text:str = 'Menu Button', options: Tuple[str] = ('Option 1', 'Option 2', 'Option 3'), font: Tuple = ('San Francisco', 10),
                 width: int = 100, height: int = 30, radius: int = 15, 
                 color: str = '#4A4A4A', hover_color: str = '#343434', active_color:str = '#2A2A2A', option_color:str = '#3A3A3A',
                 fg: str = '#FFFFFF', bg: str = '', command: Optional[Callable] = None):
        
        # -- Initialization -- #
        self.parent = parent
        self.width = width
        self.height = height
        self.text = text
        self.options = options
        self.font = font
        self.r = radius
        self.color = color
        self.hover_color = hover_color
        self.active_color = active_color
        self.option_color = option_color
        self.bg = bg or self._get_parent_bg()
        self.fg = fg
        self.command = command
        self.is_open = False
        self.selected_options: List[str] = []
        self.dropdown_window = None
        self.mouse_on_widget = False

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)

        self._draw()
        self._binds()

    def _draw(self):
        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.color, tags='btn_rect')
        self.c.create_text(10, self.height//2, text=self.text, font=self.font, fill=self.fg, anchor='w', tags='btn_text')
        self.c.create_line(self.width-18, self.height//2+4, self.width-10, self.height//2-4, width=2, fill=self.fg)
        self.c.create_line(self.width-18, self.height//2+4, self.width-26, self.height//2-4, width=2, fill=self.fg)
        self.c.create_rectangle(0, 0, self.width, self.height, fill='', outline='', tags='hitbox')

    def _binds(self):
        self.c.tag_bind('hitbox', '<Enter>', lambda e: self._btn_hover('enter'))
        self.c.tag_bind('hitbox', '<Leave>', lambda e: self._btn_hover('leave'))
        self.c.tag_bind('hitbox', '<Button-1>', lambda e: self._btn_click('click'))
        self.c.tag_bind('hitbox', '<ButtonRelease-1>', lambda e: self._btn_click('release'))

    def _btn_click(self, state: str):
        if state == 'release':
            if self.is_open:
                self.close_dropdown()
            else:
                self.open_dropdown()
        elif state == 'click':
            self

    def _btn_hover(self, state: str):        
        fill_color = self.hover_color if state == 'enter' else self.color
        self.c.itemconfig('btn_rect', fill=fill_color)

    def open_dropdown(self):
        if self.dropdown_window:
            return

        x, y = self.c.winfo_rootx(), self.c.winfo_rooty() + self.height

        self.dropdown_window = tk.Toplevel(self.parent)
        self.dropdown_window.geometry(f"{self.width}x{len(self.options)*30}+{x}+{y}")
        self.dropdown_window.overrideredirect(True)
        self.dropdown_window.configure(bg=self.color)

        for option in self.options:

            option_canvas = tk.Canvas(self.dropdown_window, width=self.width, height=30, bg=self.bg, highlightthickness=0)
            option_canvas.pack(fill='x')

            create_rounded_rectangle(option_canvas, 0, 0, self.width, 30, radius=self.r, fill=self.option_color, tags='option_rect')
            option_canvas.create_text(35, 15, text=option, font=self.font, fill=self.fg, anchor='w')

            create_rounded_rectangle(option_canvas, 5, 5, 25, 25, 10, fill=self.option_color, outline='#9A9A9A')

            if option in self.selected_options:
                option_canvas.create_line(8, 15, 13, 20, width=2, fill=self.fg)
                option_canvas.create_line(13, 20, 22, 11, width=2, fill=self.fg)

            option_canvas.create_rectangle(0, 0, self.width, 30, fill='', outline='', tags='hitbox')

            option_canvas.tag_bind('hitbox', '<Enter>', lambda e, canvas=option_canvas: self._option_hover(canvas, 'enter'))
            option_canvas.tag_bind('hitbox', '<Leave>', lambda e, canvas=option_canvas: self._option_hover(canvas, 'leave'))
            option_canvas.tag_bind('hitbox', '<Button-1>', lambda e, opt=option: self.toggle_option(opt))

        self.is_open = True
        self.dropdown_window.bind("<Enter>", self.on_enter)
        self.dropdown_window.bind("<Leave>", self.on_leave)
        self.dropdown_window.bind("<FocusOut>", self.check_focus)

    def close_dropdown(self):
        if self.dropdown_window:
            self.dropdown_window.destroy()
            self.dropdown_window = None
            self.is_open = False

    def on_enter(self, event):
        self.mouse_on_widget = True

    def on_leave(self, event):
        self.mouse_on_widget = False
        self.dropdown_window.after(100, self.check_focus)

    def check_focus(self, event=None):
        if not self.mouse_on_widget and self.dropdown_window:
            self.close_dropdown()

    def toggle_option(self, option):
        if option in self.selected_options:
            self.selected_options.remove(option)
        else:
            self.selected_options.append(option)
        
        self.close_dropdown()
        self.open_dropdown()
        
        if self.command:
            self.command(self.selected_options)

    def _option_hover(self, canvas, state):
        fill_color = self.hover_color if state == 'enter' else self.option_color
        canvas.itemconfig('option_rect', fill=fill_color)

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