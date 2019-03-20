from tkinter import *
from tkinter.filedialog import *
import numpy as np
import cv2
from PIL import Image, ImageTk


class MainFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.master.title("Example")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W + E + N + S)

        self.button = Button(self, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=1, column=0, sticky=W)

    def load_file(self):
        fname = askopenfilename(title='Please select one (any) frame from your set of images.',
                                filetypes=[('Image Files', ['.jpeg', '.jpg', '.png', '.gif',
                                                            '.tiff', '.tif', '.bmp'])])
        print(fname)
        img_array = cv2.imread(fname + "")
        img = PhotoImage(Image.fromarray(img_array))
        self.b2 = Button(self, justify=LEFT)
        self.b2.config(image=img, widht="100", height="100")
        self.b2.pack(side=RIGHT)

