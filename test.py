from tkinter import *

class Colors(Frame):
    def __init__(self):
        Frame.__init__(self)
        self._image = PhotoImage(file="assets/#FFFFFF_down_arrow.png")
        self._imageLabel = Label(self, image=self._image)
        self._imageLabel.grid()

        self.master.title("Color Changer")
        self.grid()

        self.red = Scale(self, from_=0, to=255, label="Red", fg="red", )
        self.red.grid(row=0, column=1)

        self.green = Scale(self, from_=0, to=255, label="Green", fg='green')
        self.green.grid(row=0, column=2)

        self.blue = Scale(self, from_=0, to=255, label="Blue", fg="blue")
        self.blue.grid(row=0, column=3)

        self.button = Button(self, text="Change Colors", command=self.changeColor)
        self.button.grid(row=1, column=2)

    def changeColor(self):
        red = self.red.get()
        blue = self.blue.get()
        green = self.green.get()
        for y in range(self._image.height()):
            for x in range(self._image.width()):
                self._image.put("#%02x%02x%02x" % (red,green,blue), (x, y))

def main():
    Colors().mainloop()

main()