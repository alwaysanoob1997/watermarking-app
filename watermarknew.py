import math
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from tkinter import messagebox

PRIMARY_FILETYPES = [
    ('JPG Files', '*.jpg'),
    ('JPEG Files', '*.jpeg'),
    ('PNG Files', '*.png'),
    ('BMP Files', '*.bmp')
]

WM_FILETYPES = [
    ('JPG Files', '*.jpg'),
    ('JPEG Files', '*.jpeg'),
    ('PNG Files', '*.png')
]


class ImageManager():
    def __init__(self):
        self.PHOTOPATH = None
        self.image = None
        self.wm_image = None
        self.xpos = 60
        self.ypos = 60
        self.opacity = 80
        self.size = 50
        self.sliderx = None
        self.slidery = None
        self.slidero = None
        self.sliders = None
        self.image_thumb = (300, 300)
        self.wm_thumb_size = (100, 100)
        self.last_wm_thumb_size = (100, 100)
        self.wm_w_factor= None
        self.wm_h_factor= None
        self.edit = None
        self.add_button = None

    # show the image as a thumbnail
    def get_image(self):
        # restrict file types
        path = fd.askopenfilename(title="Choose the image" ,filetypes=PRIMARY_FILETYPES)
        self.PHOTOPATH = path

        # Close any image files if previously opened and not closed(happens if i havent clicked the save button)
        if self.image:
            self.image.close()

        # if the user has not selected any file
        if not path:
            return

        # open the image and resize it to an acceptable size to view
        self.image = Image.open(path)
        self.image.thumbnail(self.image_thumb, Image.Resampling.LANCZOS)


        # has to be made global for some reason
        global img
        img = ImageTk.PhotoImage(self.image)

        # change the image displayed
        future_img.config(image=img)

        # forget the old button and display a new one
        disabled.grid_forget()
        self.add_button = ttk.Button(root, text="Open Watermark", command=self.get_wm_image)
        self.add_button.grid(column=1, row=1)

    # add functionality to superimpose 2nd image over first
    def get_wm_image(self):
        # restrict image files
        path = fd.askopenfilename(title="Choose the watermark" ,filetypes=WM_FILETYPES)

        # close the image if previously opened, unsaved image
        if self.wm_image:
            self.wm_image.close()

        # if the user has not selected any file
        if not path:
            return

        # call the edit screen only if the user has given a file
        self.edit_screen()

        # open a new image
        self.wm_image = Image.open(path)

        # opacity
        # Convert the watermark image to rgba
        if self.wm_image.mode != 'RGBA':
            self.wm_image = self.wm_image.convert("RGBA")


        # copy the watermark image for manipulation
        thumbimg = self.wm_image.copy()
        # set the size according to the last availabe size
        thumbimg.thumbnail(self.last_wm_thumb_size, Image.Resampling.LANCZOS)

        # save the height and width factors for future use.
        imght, imgwdth = self.image.size
        thmht, thmwdth = thumbimg.size
        self.wm_w_factor = imgwdth / thmwdth
        self.wm_h_factor = imght / thmht


        # position the watermark image and paste it on the actual image thumbnail
        pos = (math.floor(self.image.width * self.xpos/100), math.floor(self.image.height * self.ypos/100))

        # apply opacity
        # set the opacity according to the last saved opacity
        paste_mask = thumbimg.split()[3].point(lambda i: math.floor(i * self.opacity / 100))

        # Copy the main image and paste it on it
        copy_image = self.image.copy()
        copy_image.paste(thumbimg, pos, mask=paste_mask)

        # has to be made global
        global newimg
        newimg = ImageTk.PhotoImage(copy_image)

        # update the image
        future_img.config(image=newimg)
        future_img.update()

        # Closing the copied image
        thumbimg.close()

    # the window for editing the watermark image
    def edit_screen(self):
        self.edit = Toplevel()
        self.edit.minsize(100, 300)
        self.edit.config(padx=20, pady=10)
        self.edit.geometry("+300+200")
        self.edit.title("Editor")
        self.edit.iconbitmap("editor.ico")

        # X axis label and slider
        lblx = ttk.Label(self.edit, text="Position on X-axis")
        lblx.grid(column=0, row=0)

        self.sliderx = ttk.Scale(self.edit, from_=0, to=100, orient="h")
        self.sliderx.set(self.xpos)
        self.sliderx.grid(column=1, row=0, padx=10, pady=20)

        # Y axis label and slider
        lbly = ttk.Label(self.edit, text="Position on Y-axis")
        lbly.grid(column=0, row=1)

        self.slidery = ttk.Scale(self.edit, from_=0, to=100, orient="h")
        self.slidery.set(self.ypos)
        self.slidery.grid(column=1, row=1, pady=20)

        # Opacity label and slider
        lblop = ttk.Label(self.edit, text="Opacity")
        lblop.grid(column=0, row=2, pady=20)

        self.slidero = ttk.Scale(self.edit, from_=5, to=100, orient="h")
        self.slidero.set(self.opacity)
        self.slidero.grid(column=1, row=2, pady=20)

        # Size label and slider
        sizelbl = ttk.Label(self.edit, text="Size")
        sizelbl.grid(column=0, row=3)

        self.sliders = ttk.Scale(self.edit, from_=20, to=100, orient="h")
        self.sliders.set(self.size)
        self.sliders.grid(column=1, row=3, pady=20)

        # View changes and save buttons
        ttk.Button(self.edit, text="View Changes", command=self.view_changes).grid(column=0, row=5)
        ttk.Button(self.edit, text="Save file", command=self.save_file).grid(column=1, row=5)


    # show the image with updated changes
    def view_changes(self):
        # updating the x and y coord, opacity in the class so as to preserve the setting for further edits and to utilise it in other functions
        self.xpos = self.sliderx.get()
        self.ypos = self.slidery.get()
        self.opacity = self.slidero.get()

        # get position using the percent x and y coord by multiplying with the image dimensions
        pos = (math.floor(self.image.width * self.xpos / 100), math.floor(self.image.height * self.ypos / 100))

        # Get the factor for change in size of watermark image. Separate variable required for last changed thumbsize
        self.size = self.sliders.get()
        factor = self.sliders.get() / 50
        self.last_wm_thumb_size = tuple([math.floor(x * factor) for x in self.wm_thumb_size])

        # copy the watermark image
        thumbimg = self.wm_image.copy()
        # update size of thumbimg using last size factor
        thumbimg.thumbnail(self.last_wm_thumb_size, Image.Resampling.LANCZOS)

        # update the width and height factor for the images each time
        imgwdth, imght = self.image.size
        thmwdth, thmht = thumbimg.size
        self.wm_w_factor = imgwdth / thmwdth
        self.wm_h_factor = imght / thmht


        # update the opacity
        paste_mask = thumbimg.split()[3].point(lambda i: math.floor(i * self.opacity / 100))

        # paste the watermark image on a copy of the image to show for user experience
        copy_image = self.image.copy()
        copy_image.paste(thumbimg, pos, mask=paste_mask)

        # has to be made global for it to display
        global newnewimg
        newnewimg = ImageTk.PhotoImage(copy_image)
        future_img.config(image=newnewimg)
        future_img.update()

        # No further operations on the copied images, and therefore can be closed
        copy_image.close()
        thumbimg.close()

    # add functionality to save image as new file
    def save_file(self):
        # close the image as it was saved as a thumbnail image
        self.image.close()

        # open it again as full size
        with Image.open(self.PHOTOPATH) as fullphoto:
            # Get new position based on the last saved x and y coord
            fullwdth, fullht = fullphoto.size
            newpos = (math.floor(fullwdth * self.xpos / 100), math.floor(fullht * self.ypos / 100))

            # calculate the watermark image's new size when compared to the full image
            # Has to be done as previously we were only calculating it for a smaller image
            newsize = (fullwdth/self.wm_w_factor, fullht/self.wm_h_factor)


            # Create a new watermark image and paste it onto the full image at the correct position
            self.wm_image.thumbnail(newsize, Image.Resampling.LANCZOS)

            # update the opacity
            paste_mask = self.wm_image.split()[3].point(lambda i: math.floor(i * self.opacity / 100))
            # save the image with thw reduced opacity if mentioned
            fullphoto.paste(self.wm_image, newpos, mask=paste_mask)

            # Create a new file by altering the filepath by splitting using the '/' nad joining again
            newpathlist = self.PHOTOPATH.split("/")
            newfilename = "wm_" + newpathlist[-1]
            newpath = "/".join(newpathlist[:-1] + [newfilename])

            # save image
            fullphoto.save(newpath)

        messagebox.showinfo(title="Image Saved", message=f"Image has been saved to {newpath}")

        # close the watermark image now
        self.wm_image.close()
        # Close the edit screen
        self.edit.destroy()

        # change the image displayed to none
        future_img.config(image='')
        future_img.update()

        # Disable the add watermark button again
        self.add_button.grid_forget()
        disabled.grid(column=1, row=1)




manager = ImageManager()

# create a tkinter window
root = Tk()
root.geometry("+600+200")
root.minsize(400, 300)
root.title("Watermarking App")
root.config(pady=15, padx=15)
root.iconbitmap("main.ico")


imgframe = Frame(root)
imgframe.grid(column=0, row=0, rowspan=2, sticky=(N, S, E, W))

future_img = ttk.Label(imgframe, text="Image Here")
future_img.grid()


ttk.Button(root, text="Open Photo", command=manager.get_image).grid(column=1, row=0)
disabled = ttk.Button(root, text="Open Watermark", state=DISABLED)
disabled.grid(column=1, row=1)


root.columnconfigure(0, weight=2)
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

imgframe.columnconfigure(0, weight=2)
imgframe.rowconfigure(0, weight=1)


root.mainloop()

