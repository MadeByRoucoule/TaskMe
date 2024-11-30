# -- Imports -- #
import tkinter as tk
from typing import Tuple, Optional, Callable, List
import math

# -- Utility Functions -- #
def create_rounded_rectangle(canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, radius: int, **kwargs) -> int:
    points = [
        x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
        x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
        x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
        x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# -- TaskWidget Class -- #
class TaskWidget():
    def __init__(self, parent, text: str, date: str, hour: str, priority: str,
                 font: Tuple[str, int] = ('San Francisco', 10), width: int = 200, height: int = 100,
                 r: int = 25, color: str = '', fg: str = '#FFFFFF', bg: str = '', priority_colors: list = ['#3E2825', '#403324', '#23312A']):

        # -- Initialization -- #
        self.parent = parent
        self.width = width
        self.height = height
        self.text = text
        self.date = date
        self.hour = hour
        self.priority = priority
        self.font = font
        self.r = r
        self.color = color
        self.fg = fg
        self.bg = bg or self._get_parent_bg()
        self.priority_color = priority_colors

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)

        # -- Drawing Elements -- #
        if not self.color and self.priority == 'High':
            create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.priority_color[0])
        elif not self.color and self.priority == 'Medium':
            create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.priority_color[1])
        elif not self.color and self.priority == 'Low':
            create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.priority_color[2])
        
        self.c.create_text(15, 15, text=self.text, fill=self.fg, font=('San Francisco', 12, 'bold'), width=self.width-15*2, anchor='nw')
        self.c.create_text(10, self.height-10, text=self.date, fill=self.fg, font=self.font, anchor='sw')
        self.c.create_text(80, self.height-10, text=self.hour, fill=self.fg, font=self.font, anchor='sw')
        self.c.create_text(self.width-10, self.height-10, text=self.priority, fill=self.fg, font=('San Francisco', 10, 'bold'), anchor='se')
    
    # -- Utility Methods -- #
    def _get_parent_bg(self) -> str:
        window_color = self.parent.cget('bg')
        rgb_values = self.parent.winfo_rgb(window_color)
        return '#{:02x}{:02x}{:02x}'.format(rgb_values[0] // 256, rgb_values[1] // 256, rgb_values[2] // 256)

    # -- Layout Methods -- #
    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)

# -- Button Class -- #
class Button():
    def __init__(self, parent, text: str = 'Button', font: Tuple[str, int] = ('San Francisco', 10),
                 width: int = 100, height: int = 30, r: int = 30, color: str = '#3C3C3C',
                 hover_color: str = '#4C4C4C', fg: str = '#FFFFFF', bg: str = '', command: Optional[Callable] = None):
        
        # -- Initialization -- #
        self.parent = parent
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.r = r
        self.color = color
        self.hover_color = hover_color
        self.bg = bg or self._get_parent_bg()
        self.fg = fg
        self.command = command

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)

        # -- Drawing Elements -- #
        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.color, tags='btn_rect')
        self.c.create_text(self.width // 2, self.height // 2, text=self.text, font=self.font, fill=self.fg, tags='btn_text')
        self.c.create_rectangle(0, 0, width, height, fill='', outline='', tags='hitbox')

        # -- Event Bindings -- #
        self.c.tag_bind('hitbox', '<Enter>', lambda e: self._btn_hover('enter'))
        self.c.tag_bind('hitbox', '<Leave>', lambda e: self._btn_hover('leave'))
        self.c.tag_bind('hitbox', '<Button-1>', lambda e: self._btn_click('click'))
        self.c.tag_bind('hitbox', '<ButtonRelease-1>', lambda e: self._btn_click('release'))

    # -- Event Handlers -- #
    def _btn_click(self, state: str):
        if state == 'release' and self.command:
            self.command()

    def _btn_hover(self, state: str):
        fill_color = self.hover_color if state == 'enter' else self.color
        self.c.itemconfig('btn_rect', fill=fill_color)

    # -- Utility Methods -- #
    def _get_parent_bg(self) -> str:
        window_color = self.parent.cget('bg')
        rgb_values = self.parent.winfo_rgb(window_color)
        return '#{:02x}{:02x}{:02x}'.format(rgb_values[0] // 256, rgb_values[1] // 256, rgb_values[2] // 256)

    # -- Layout Methods -- #
    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)

# -- Entry Class -- #
class Entry():
    def __init__(self, parent, font: Tuple[str, int] = ('San Francisco', 10),
                 placeholder_text: str = 'Entry', placeholder_color: str = '#888888',
                 width: int = 100, height: int = 30, r: int = 30, color: str = '#4C4C4C',
                 fg: str = '#FFFFFF', bg: str = '', border_color: str = '#343434',
                 border_width: int = 2, entry_width: int = 20):

        # -- Initialization -- #
        self.parent = parent
        self.width = width
        self.height = height
        self.font = font
        self.placeholder_text = placeholder_text
        self.placeholder_color = placeholder_color
        self.r = r
        self.color = color
        self.fg = fg
        self.bg = bg or self._get_parent_bg()
        self.border_color = border_color
        self.border_width = border_width
        self.entry_width = round(self.width/9)
        
        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)

        # -- Entry Widget Creation -- #
        self.e = tk.Entry(self.parent, relief=tk.FLAT, highlightthickness=0, bg=self.color, font=self.font, fg=self.fg, width=self.entry_width)
        self.e.insert(0, self.placeholder_text)
        self.e.bind("<FocusIn>", self._on_entry_click)
        self.e.bind("<FocusOut>", self._on_focusout)
        self.e.config(fg=self.placeholder_color)
        self.c.create_window(self.width // 2, self.height // 2, window=self.e, anchor='center', tags='entry_window')

        # -- Drawing Elements -- #
        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.border_color, tags='border_rect')
        create_rounded_rectangle(self.c, self.border_width, self.border_width, self.width-self.border_width, self.height-self.border_width, radius=self.r, fill=self.color, tags='entry_rect')
        self.c.create_rectangle(0, 0, width, height, fill='', outline='', tags='hitbox')

        # -- Event Bindings -- #
        self.c.tag_bind('hitbox', '<Button-1>', self._on_entry_click)

    # -- Event Handlers -- #
    def _on_entry_click(self, event):
        if self.e.get() == self.placeholder_text:
            self.e.focus()
            self.e.delete(0, "end")
            self.e.insert(0, '')
            self.e.config(fg=self.fg)

    def _on_focusout(self, event):
        if self.e.get() == '':
            self.e.insert(0, self.placeholder_text)
            self.e.config(fg=self.placeholder_color)

    # -- Getter and Setter -- #
    def get(self) -> str:
        return '' if self.e.get() == self.placeholder_text else self.e.get()

    def set(self, value: str):
        self.e.delete(0, tk.END)
        self.e.insert(0, value)
        self.e.config(fg=self.fg if value else self.placeholder_color)
        if not value:
            self.e.insert(0, self.placeholder_text)

    # -- Utility Methods -- #
    def _get_parent_bg(self) -> str:
        window_color = self.parent.cget('bg')
        rgb_values = self.parent.winfo_rgb(window_color)
        return '#{:02x}{:02x}{:02x}'.format(rgb_values[0] // 256, rgb_values[1] // 256, rgb_values[2] // 256)

    # -- Layout Methods -- #
    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)

# -- MenuButton Class -- #
class MenuButton:
    def __init__(self, parent, text: str = 'Button', options: List[str] = [], 
                 font: Tuple[str, int] = ('San Francisco', 10),
                 width: int = 100, height: int = 30, r: int = 30, 
                 color: str = '#3C3C3C', hover_color: str = '#4C4C4C', 
                 fg: str = '#FFFFFF', bg: str = '', 
                 command: Optional[Callable] = None):
        
        # -- Initialization -- #
        self.parent = parent
        self.width = width
        self.height = height
        self.text = text
        self.options = options
        self.font = font
        self.r = r
        self.color = color
        self.hover_color = hover_color
        self.bg = bg or self._get_parent_bg()
        self.fg = fg
        self.command = command
        self.is_open = False
        self.selected_option = None

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, 
                           bg=self.bg, highlightthickness=0)

        # -- Drawing Elements -- #
        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, 
                                 radius=self.r, fill=self.color, tags='btn_rect')
        self.c.create_text(10, self.height//2, text=self.text, fill=self.fg, 
                           anchor='w', tags='btn_text', font=self.font)
        self._draw_triangle()
        self.c.create_rectangle(0, 0, self.width, self.height, 
                                fill='', outline='', tags='hitbox')

        # -- Event Bindings -- #
        self.c.tag_bind('hitbox', '<Enter>', lambda e: self._btn_hover('enter'))
        self.c.tag_bind('hitbox', '<Leave>', lambda e: self._btn_hover('leave'))
        self.c.tag_bind('hitbox', '<Button-1>', lambda e: self._btn_click())

        self.dropdown = None

    # -- Triangle Drawing -- #
    def _draw_triangle(self):

        triangle_width = min(self.height // 2, self.width // 8)
        triangle_height = triangle_width // 2

        x_center = self.width - 20
        y_center = self.height // 2

        x1 = x_center - triangle_width / 2
        x2 = x_center + triangle_width / 2
        x3 = x_center

        y1 = y_center - triangle_height / 2
        y2 = y_center - triangle_height / 2
        y3 = y_center + triangle_height / 2

        self.c.create_polygon(x1, y1, x2, y2, x3, y3, 
                            fill=self.fg, outline=self.fg, tags='down_arrow')

    # -- Event Handlers -- #
    def _btn_click(self):
        if self.is_open:
            self.close_dropdown()
        else:
            self.open_dropdown()

    def _btn_hover(self, state: str):
        fill_color = self.hover_color if state == 'enter' else self.color
        self.c.itemconfig('btn_rect', fill=fill_color)

    def _option_selected(self, option: str):
        self.selected_option = option
        if self.dropdown:
            self.dropdown.update_selected() 
        if self.command:
            self.command(option)
        self.close_dropdown()

    # -- Dropdown Management -- #
    def open_dropdown(self):
        if self.dropdown is None or not self.dropdown.winfo_exists():
            x = self.parent.winfo_rootx() + self.c.winfo_x()
            y = self.parent.winfo_rooty() + self.c.winfo_y() + self.height
            self.dropdown = DropdownWindow(self.parent, self.options, self.width, 
                                           self.font, self.color, self.hover_color, 
                                           self.fg, self._option_selected, 
                                           selected_option=self.selected_option)
            dropdown_height = len(self.options) * 30 + 4
            self.dropdown.geometry(f"{self.width}x{dropdown_height}+{x}+{y}")
        else:
            self.dropdown.selected_option = self.selected_option
            self.dropdown.update_selected()
        self.dropdown.deiconify()
        self.is_open = True

    def close_dropdown(self):
        if self.dropdown and self.dropdown.winfo_exists():
            self.dropdown.withdraw()
        self.is_open = False

    # -- Utility Methods -- #
    def _get_parent_bg(self) -> str:
        window_color = self.parent.cget('bg')
        rgb_values = self.parent.winfo_rgb(window_color)
        return '#{:02x}{:02x}{:02x}'.format(rgb_values[0] // 256, 
                                            rgb_values[1] // 256, 
                                            rgb_values[2] // 256)

    # -- Layout Methods -- #
    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)

# -- DropdownWindow Class -- #
class DropdownWindow(tk.Toplevel):
    def __init__(self, parent, options: List[str], width: int, 
                 font: Tuple[str, int], color: str, hover_color: str, 
                 fg: str, command: Callable, selected_option: Optional[str] = None):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self.width = width
        self.height = len(options) * 30 + 4
        self.color = color
        self.hover_color = hover_color
        self.fg = fg
        self.font = font
        self.command = command
        self.selected_option = selected_option
        self.options = options
        self.buttons = []

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, 
                                bg=parent.cget('bg'), highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        create_rounded_rectangle(self.canvas, 2, 2, self.width-2, self.height-2, 
                                 radius=10, fill=self.color, outline='')

        self.create_buttons()

        self.bind('<FocusOut>', self._on_focus_out)

    def create_buttons(self):
        for i, option in enumerate(self.options):
            y = i * 30 + 2
            button = tk.Button(self.canvas, text=option, font=self.font, 
                               bg=self.color, fg=self.fg,
                               activebackground=self.hover_color, 
                               activeforeground=self.fg,
                               relief=tk.FLAT, anchor='w',
                               command=lambda o=option: self._on_select(o))
            button.configure(width=self.width-4)
            
            self.canvas.create_window(self.width//2, y+15, window=button, width=self.width-4)
            
            button.bind("<Enter>", lambda e, b=button: self._on_enter(b))
            button.bind("<Leave>", lambda e, b=button: self._on_leave(b))
            
            self.buttons.append(button)
        
        self.update_selected()

    def update_selected(self):
        for button in self.buttons:
            if button['text'] == self.selected_option:
                button.configure(text="✓ " + button['text'])
            elif button['text'].startswith("✓ "):
                button.configure(text=button['text'][2:])

    def _on_select(self, option):
        self.selected_option = option
        self.update_selected()
        self.command(option)
        self.withdraw()

    def _on_enter(self, button):
        button.config(bg=self.hover_color)

    def _on_leave(self, button):
        button.config(bg=self.color)

    def _on_focus_out(self, event):
        self.withdraw()