import tkinter as tk

class TaskWidget():
    def __init__(self, parent, width=150, height=100, r=25, color='#399399', fg='#FFFFFF', bg='#2B2B2B'):

        self.parent = parent
        self.width = width
        self.height = height
        self.r = r
        self.color = color
        self.fg = fg
        self.bg = bg
        
        self.c = tk.Canvas(self.parent, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        
        self.create_rounded_rectangle(self.c, 0, 0, self.width, self.height, radius=self.r, fill=self.color)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
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
    
    def pack(self, **kwargs):
        self.c.pack(**kwargs)
    
    def place(self, **kwargs):
        self.c.place(**kwargs)

    def grid(self, **kwargs):
        self.c.grid(**kwargs)