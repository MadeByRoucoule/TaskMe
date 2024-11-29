import tkinter as tk
import platform

class TaskWidget():
    def __init__(self, parent, text, date, hour, priority, font=('San Francisco', 10), width=200, height=100, r=25, color='#399399', fg='#FFFFFF', bg=''):

        self.parent = parent
        self.text = text
        self.date = date
        self.hour = hour
        self.priority = priority
        self.font = font
        self.width = width
        self.height = height
        self.r = r
        self.color = color
        self.fg = fg
        self.bg = bg
        
        if not self.bg:
            window_color = self.parent.cget('bg')
            rgb_values = self.parent.winfo_rgb(window_color)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                rgb_values[0] // 256,
                rgb_values[1] // 256,
                rgb_values[2] // 256
            )
            self.bg = hex_color

        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        
        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.color)
        self.c.create_text(10, 10, text=self.text, fill=self.fg, font=('San Francisco', 12, 'bold'), anchor='nw')
        self.c.create_text(15, 30, text=f'Date: {self.date}', fill=self.fg, font=self.font, anchor='nw')
        self.c.create_text(15, 50, text=f'Heure : {self.hour}', fill=self.fg, font=self.font, anchor='nw')
        self.c.create_text(15, 70, text=f'Priorité : {self.priority}', fill=self.fg, font=self.font, anchor='nw')

    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)


class Button():
    def __init__(self, parent, text='Button', font=('San Francisco', 10), width=100, height=30, r=30, color='#3C3C3C', hover_color='#4C4C4C', fg='#FFFFFF', bg='', command=None):
        
        self.parent = parent
        self.text = text
        self.font = font
        self.width = width
        self.height = height
        self.r = r
        self.color = color
        self.hover_color = hover_color
        self.fg = fg
        self.bg = bg
        self.command = command
        
        if not self.bg:
            window_color = self.parent.cget('bg')
            rgb_values = self.parent.winfo_rgb(window_color)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                rgb_values[0] // 256,
                rgb_values[1] // 256,
                rgb_values[2] // 256
            )
            self.bg = hex_color

        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)

        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.color, tags='btn_rect')
        self.c.create_text(self.width // 2, self.height // 2, text=self.text, font=self.font, fill=self.fg, tags='btn_text')
        self.c.create_rectangle(0, 0, width, height, fill='', outline='', tags='hitbox')

        self.c.tag_bind('hitbox', '<Enter>', lambda e: self.btnHover('enter'))
        self.c.tag_bind('hitbox', '<Leave>', lambda e: self.btnHover('leave'))
        self.c.tag_bind('hitbox', '<Button-1>', lambda e: self.btnClick('click'))
        self.c.tag_bind('hitbox', '<ButtonRelease-1>', lambda e: self.btnClick('release'))

    def btnClick(self, state):
        if state == 'release':
            if self.command:
                self.command()

    def btnHover(self, state):
        if state == 'enter':
            self.c.itemconfig('btn_rect', fill=self.hover_color)
        elif state == 'leave':
            self.c.itemconfig('btn_rect', fill=self.color)

    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)

class Entry():
    def __init__(self, parent, 
                 font=('San Francisco', 10),
                 placeholder_text = 'Entry', 
                 placeholder_color = '#888888',
                 width=100, 
                 height=30, 
                 r=30, 
                 color='#4C4C4C', 
                 fg='#FFFFFF', 
                 bg='', 
                 border_color='#343434', 
                 border_width=2,
                 entry_width=20):

        self.parent = parent
        self.font = font
        self.placeholder_text = placeholder_text
        self.placeholder_color = placeholder_color
        self.width = width
        self.height = height
        self.r = r
        self.color = color
        self.fg = fg
        self.bg = bg or self.parent.cget('bg')
        self.border_color = border_color
        self.border_width = border_width
        self.entry_width = round(self.width/9)

        self.c = tk.Canvas(self.parent, bg=self.bg, highlightthickness=0)


        self.e = tk.Entry(self.parent, relief=tk.FLAT, highlightthickness=0, bg=self.color, font=self.font, fg=self.fg, width=self.entry_width)
        self.e.insert(0, self.placeholder_text)
        self.e.bind("<FocusIn>", self.on_entry_click)
        self.e.bind("<FocusOut>", self.on_focusout)
        self.e.config(fg=self.placeholder_color)
        self.c.create_window(self.width // 2, self.height // 2, window=self.e, anchor='center', tags='entry_window')

        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.border_color, tags='border_rect')
        create_rounded_rectangle(self.c, self.border_width, self.border_width, self.width-self.border_width, self.height-self.border_width, radius=self.r, fill=self.color, tags='entry_rect')
        self.c.create_rectangle(0, 0, width, height, fill='', outline='', tags='hitbox')

        self.c.tag_bind('hitbox', '<Button-1>', self.on_entry_click)

    def on_entry_click(self, event):
        if self.e.get() == self.placeholder_text:
            self.e.focus()
            self.e.delete(0, "end")
            self.e.insert(0, '')
            self.e.config(fg=self.fg)

    def on_focusout(self, event):
        if self.e.get() == '':
            self.e.insert(0, self.placeholder_text)
            self.e.config(fg=self.placeholder_color)

    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)

    def get(self):
        if self.e.get() == self.placeholder_text:
            return ''
        return self.e.get()

    def set(self, value):
        self.e.delete(0, tk.END)
        self.e.insert(0, value)
        if value:
            self.e.config(fg=self.fg)
        else:
            self.e.insert(0, self.placeholder_text)
            self.e.config(fg=self.placeholder_color)

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
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