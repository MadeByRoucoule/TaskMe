import tkinter as tk

class TaskWidget():
    def __init__(self, parent, width=150, height=100, r=25, color='#399399', fg='#FFFFFF', bg='#1B1B1B'):

        self.parent = parent
        self.width = width
        self.height = height
        self.r = r
        self.color = color
        self.fg = fg
        self.bg = bg
        
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        
        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.color)
    
    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)


class Button():
    def __init__(self, parent, text='Button', font=('San Francisco', 10), width=100, height=30, r=30, color='#399399', fg='#FFFFFF', bg='#1B1B1B', command=None):
        
        self.parent = parent
        self.text = text
        self.font = font
        self.width = width
        self.height = height
        self.r = r
        self.color = color
        self.fg = fg
        self.bg = bg
        self.command = command
        
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)

        create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.color, tags='btn_rect')
        self.c.create_text(self.width // 2, self.height // 2, text=self.text, font=self.font, fill=self.fg, tags='btn_text')
        self.c.create_rectangle(0, 0, width, height, fill='', outline='', tags='hitbox')

        self.c.tag_bind('hitbox', '<Button-1>', lambda e: self.btnClick('click'))
        self.c.tag_bind('hitbox', '<ButtonRelease-1>', lambda e: self.btnClick('release'))

    def btnClick(self, state):
        if state == 'release':
            if self.command:
                self.command()

    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)


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