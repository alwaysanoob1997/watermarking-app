from tkinter import *

root = Tk()


def drag(event):
    event.widget.place(x=event.x_root, y=event.y_root,anchor=CENTER)



card = Canvas(root, width=50, height=50, bg='blue')
card.place(x=300, y=600,anchor=CENTER)


card.bind("<B1-Motion>", drag)


root.mainloop()