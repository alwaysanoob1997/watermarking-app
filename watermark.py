from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import time

PHOTO = None
WATERMARK = None


# add file open functionality
def get_img_path():
    path = fd.askopenfilename()
    global img
    global future_img

    global PHOTO
    PHOTO = path

    rawimg = Image.open(path)
    width, height = rawimg.size
    print(width, height)

    rawimg.thumbnail((300,300), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(rawimg)


    future_img.grid_forget()
    future_img = ttk.Label(frame, image=img)
    future_img.grid(column=0, row=0, rowspan=2)
    future_img.update()

    # global wmframe
    # wmframe = ttk.Frame(future_img)
    # wmframe.grid(sticky=(N, S, E, W))

    print(future_img.winfo_geometry())
    ttk.Button(frame, text="Open Watermark", command=get_wm_path).grid(column=1, row=1, sticky=E)

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
root.geometry("+450+200")
root.minsize(400, 300)
root.title("Watermarking App")

frame = ttk.Frame(root, padding=10)
frame.grid(sticky=(N, S, E, W))

future_img = ttk.Label(frame, text="Image Here")
future_img.grid(column=0, row=0, rowspan=2)


ttk.Button(frame, text="Open Photo", command=get_img_path).grid(column=1, row=0, sticky=E)
ttk.Button(frame, text="Open Watermark", state=DISABLED).grid(column=1, row=1, sticky=E)

# todo add functionality to superimpose 2nd image over first




root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=2)
frame.columnconfigure(1, weight=1)


frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)





# todo lower opacity using pillow

# todo add functionality to save image as new file

# todo add functionality to select from one of predefined areas for watermark


root.mainloop()

