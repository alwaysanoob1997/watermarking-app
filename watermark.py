from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import time

PHOTO = None
WATERMARK = None


def drag(event):
    event.widget.place(x=event.x_root, y=event.y_root,anchor=CENTER)

# add file open functionality
def get_img_path():
    path = fd.askopenfilename()

    global PHOTO
    PHOTO = path

    rawimg = Image.open(path)
    width, height = rawimg.size
    print(width, height)

    global img
    rawimg.thumbnail((300,300), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(rawimg)

    global future_img
    global imgframe
    # future_img.grid_forget()
    # future_img = ttk.Label(imgframe, image=img)
    # future_img.place()
    future_img.config(image=img)
    future_img.update()
    future_img.bind("<B1-Motion>", drag)

    print(future_img.winfo_geometry())
    ttk.Button(bframe, text="Open Watermark", command=get_wm_path).grid(column=1, row=1, sticky=E)

def get_wm_path():
    path = fd.askopenfilename()
    global WATERMARK
    WATERMARK = path

    global wmimg
    wm_rawimg = Image.open(path)
    wm_rawimg.thumbnail((100, 100), Image.Resampling.LANCZOS)
    wmimg = ImageTk.PhotoImage(wm_rawimg)

    wm_lbl = ttk.Label(future_img, image=wmimg)
    wm_lbl.grid(column=0, row=0, rowspan=2)
    wm_lbl.update()
    print("Watermark added")


# create a tkinter window
root = Tk()
root.geometry("+600+200")
root.minsize(400, 300)
root.title("Watermarking App")

imgframe = Canvas(root)
imgframe.grid(column=0, row=0, rowspan=2, sticky=(N, S, E, W))

bframe = ttk.Frame(root, padding=10)
bframe.grid(column=1, row=0, rowspan=2, sticky=(N, S, E, W))

future_img = ttk.Label(imgframe, text="Image Here")
future_img.grid(column=0, row=0, rowspan=2)


ttk.Button(bframe, text="Open Photo", command=get_img_path).grid(column=1, row=0, sticky=E)
ttk.Button(bframe, text="Open Watermark", state=DISABLED).grid(column=1, row=1, sticky=E)


# todo add functionality to superimpose 2nd image over first




root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
imgframe.columnconfigure(0, weight=2)
imgframe.columnconfigure(1, weight=1)


imgframe.rowconfigure(0, weight=1)
imgframe.rowconfigure(1, weight=1)





# todo lower opacity using pillow

# todo add functionality to save image as new file

# todo add functionality to select from one of predefined areas for watermark


root.mainloop()

