# -- Imports -- #
import tkinter as tk
from typing import Tuple, Optional, Callable, List

# -- Utility Functions -- #
def create_rounded_rectangle(canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, radius: int, **kwargs) -> int:
    points = [
        x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
        x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
        x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
        x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
    ]
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

class Entry:
    def __init__(self, parent, font:Tuple[str, int] = ('San Francisco', 10), placeholder_text:str = 'Entry', 
                 width:int = 100, height:int = 30, radius:int = 15, border_width: int = 2,
                 color: str = '#4C4C4C', fg: str = '#FFFFFF',placeholder_color:str = '#888888',
                 bg: str = '', border_color: str = '#343434'):
        
        # -- Initialization -- #
        self.parent = parent
        self.font = font
        self.font_list = tuple(font)
        self.placeholder_text = placeholder_text
        self.width = width
        self.height = height
        self.r = radius
        self.border_width = border_width
        self.color = color
        self.fg = fg
        self.placeholder_color = placeholder_color
        self.bg = bg or self._get_parent_bg()
        self.border_color = border_color

        # -- Canvas Creation -- #
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)

        self._draw()
        self._binds()

    # -- Drawing Elements -- #
    def _draw(self):
        # -- Entry Widget Creation -- #
        self.e = tk.Entry(self.parent, relief=tk.FLAT, highlightthickness=0, bg=self.color, font=self.font, fg=self.fg)
        self.e.insert(0, self.placeholder_text)
        self.e.config(fg=self.placeholder_color)
        self.c.create_window(self.width // 2, self.height // 2, window=self.e, anchor='center', tags='entry_window', width=self.width-15, height=self.height-15)

        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.border_color, tags='border_rect')
        create_rounded_rectangle(self.c, self.border_width, self.border_width, self.width-self.border_width, self.height-self.border_width, radius=self.r-self.border_width, fill=self.color, tags='entry_rect')
        self.c.create_rectangle(0, 0, self.width, self.height, fill='', outline='', tags='hitbox')

    def _binds(self):
        self.e.bind("<FocusIn>", self._on_entry_click)
        self.e.bind("<FocusOut>", self._on_focusout)

    # -- Event Handlers -- #
    def _on_entry_click(self, event):
        if self.e.get() == self.placeholder_text:
            self.e.focus()
            self.e.delete(0, "end")
            self.e.config(fg=self.fg)

    def _on_focusout(self, event):
        if self.e.get() == '':
            self.e.insert(0, self.placeholder_text)
            self.e.config(fg=self.placeholder_color)

    def get(self):
        if self.e.get() == self.placeholder_text and self.e.cget('foreground') == self.placeholder_color:
            return ''
        else :
            return self.e.get()

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


class MenuButton:
    def __init__(self, parent, text:str = 'Menu Button', options: Tuple[str] = ('Option 1', 'Option 2', 'Option 3'), font: Tuple = ('San Francisco', 10),
                 width: int = 100, height: int = 30, radius: int = 15, 
                 color: str = '#4A4A4A', hover_color: str = '#343434', active_color:str = '#2A2A2A', 
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
        self.bg = bg or self._get_parent_bg()
        self.fg = fg
        self.command = command
        self.is_open = False
        self.selected_option = None
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
            option_canvas.pack(fill=tk.X)

            create_rounded_rectangle(option_canvas, 0, 0, self.width, 30, radius=self.r, fill=self.color, tags='option_rect')
            option_canvas.create_text(10, 15, text=option, font=self.font, fill=self.fg, anchor='w')
            option_canvas.create_rectangle(0, 0, self.width, 30, fill='', outline='', tags='hitbox')

            option_canvas.tag_bind('hitbox', '<Enter>', lambda e, canvas=option_canvas: self._option_hover(canvas, 'enter'))
            option_canvas.tag_bind('hitbox', '<Leave>', lambda e, canvas=option_canvas: self._option_hover(canvas, 'leave'))
            option_canvas.tag_bind('hitbox', '<Button-1>', lambda e, opt=option: self.select_option(opt))

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

    def select_option(self, option):
        self.selected_option = option
        self.c.itemconfig('btn_text', text=option)
        self.close_dropdown()
        if self.command:
            self.command(option)

    def _option_hover(self, canvas, state):
        fill_color = self.hover_color if state == 'enter' else self.color
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