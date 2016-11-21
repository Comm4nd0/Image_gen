#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#

"""

"""


try:
    import tkinter as tk
    from tkinter import ttk
    from io import BytesIO
    from urllib.request import urlopen
except ImportError:
    # must be python2
    import Tkinter as tk
    import ttk
    from StringIO import StringIO as BytesIO
    from urllib import urlopen

from PIL import Image, ImageTk
import praw
import os

CHOICES = ['pics', 'gifs', 'aww', 'EarthPorn', 'funny', 'nsfw']
IMG_FORMATS = ['.jpg', '.gif', '.png', '.jpeg', '.bmp']

class ImageGetter(praw.Reddit):
    def __init__(self):
        praw.Reddit.__init__(self, user_agent='gimmy pics')

        self.subreddit = None
        self.images = []

    def load_subreddit(self, subreddit):
        #makes the generator. Reddit has a limit of 1,000 results
        self.subreddit = self.get_subreddit(subreddit).get_top(limit=None)

    def get_img_url(self, num=None):
        """returns the image url from the list or the next image in the subreddit"""
        if num is None or num >= len(self.images):
            for item in self.subreddit:
                if os.path.splitext(item.url)[1] in IMG_FORMATS:
                    self.images.append(item.url)
                    return item.url
        else:
            return self.images[num]

class GUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.center(800, 650)
        self.master.configure(background='black')
        self.master.title("Images 2.0")

        # causes the full width of the window to be used
        self.columnconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        self.make_UI()
        self.r = ImageGetter()
        self.img_num = 0

    def make_UI(self):
        style = ttk.Style()
        # global style changes
        style.configure(".", background='black', foreground='white', anchor="center")
        # Button style changes
        style.map("TButton", background=[('hover', 'blue')])
        # Optionmenu. The actual menu cannot be themed :(
        style.map("TMenubutton", background=[('hover', 'blue')])

        heading = ttk.Label(self, text="IMAGES", font=("Courier", 44))
        heading.grid(column=1, row=0, rowspan=2, columnspan=2, sticky='WENS')

        intro = ttk.Label(self, font=("Courier", 12))
        intro['text']="Welcome to the image generator, select your image type below."
        intro.grid(column=1, row=2, rowspan=2, columnspan=2, sticky='WENS')

        # options
        self.var = tk.StringVar(self)
        self.var.set("Select Type")
        option = ttk.OptionMenu(self, self.var, "Select Type", *CHOICES)
        option.grid(column=1, row=4, sticky='N')

        # button
        button = ttk.Button(self, text="Get Images", command=self.create_img_list)
        button.grid(column=2, row=4, sticky='N')
        back = ttk.Button(self, text="<--", command=self.decrese_num)
        back.grid( column=1, row=5)
        forward = ttk.Button(self, text="-->", command=self.increse_num)
        forward.grid(column=2, row=5)

        # set inital holding image
        init_image = "initial.jpg"
        image = Image.open(init_image)
        self.photo = ImageTk.PhotoImage(image)
        self.img_label = ttk.Label(self, image=self.photo)
        self.img_label.grid(column=1, row=6, columnspan=2, padx=5, pady=5)

    def create_img_list(self):
        self.r.load_subreddit(self.var.get())
        self.img_num = 0
        self.get_image()

    def get_image(self):
        image_bytes = urlopen(self.r.get_img_url(self.img_num)).read()

        # internal data file
        data_stream = BytesIO(image_bytes)
        # open as a PIL image object
        image = Image.open(data_stream)
        # resize image
        wpercent = (self.winfo_width() / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((self.winfo_width(), hsize), Image.ANTIALIAS)

        self.photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=self.photo)

    def increse_num(self):
        self.img_num += 1
        self.get_image()

    def decrese_num(self):
        self.img_num -= 1
        self.get_image()

    def center(self, width, height):
        """center the window on the screen"""
        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == '__main__':
    root = tk.Tk()
    window = GUI(root)
    window.pack(fill=tk.X, expand=True, anchor=tk.CENTER)
    root.mainloop()


