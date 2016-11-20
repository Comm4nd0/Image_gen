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
    #must be python2
    import Tkinter as tk
    import ttk
    from StringIO import StringIO as BytesIO
    from urllib import urlopen

from PIL import Image, ImageTk
import praw
import os

CHOICES = ['pics', 'gifs', 'aww', 'EarthPorn', 'nsfw']
IMG_FORMATS = ['jpg', 'gif', 'png', 'jpeg', 'bmp']
basewidth = 400


DEFAULTS = {
    'bg':"black",
    'fg':"white"}
    
class Label(tk.Label):
    """a tk.Label with the DEFAULTS applied"""
    def __init__(self, master, **kwargs):
        options = DEFAULTS.copy()
        options.update(kwargs)
        tk.Label.__init__(self, master, **options)
    
class Button(tk.Button):
    """a ttk.Button with the DEFAULTS applied"""
    def __init__(self, master, **kwargs):
        options = DEFAULTS.copy()
        options.update(kwargs)
        tk.Button.__init__(self, master, **options)
        
class GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, background='black')
        
        self.center(800, 650)
        self.master.configure(background='black')
        self.master.title("Images 2.0")
        
        self.make_UI()
        self.r = praw.Reddit(user_agent='gimmy pics')
        self.img_num = 0
        self.images = None
        
    def make_UI(self):
        heading = Label(self, text="IMAGES", font=("Courier", 44))
        heading.grid(column=1, row=0, rowspan=2, columnspan=2, sticky='WENS')
        
        intro = Label(self, font=("Courier", 12))
        intro['text']="Welcome to the image generator, select your image type below."
        intro.grid(column=1, row=2, rowspan=2, columnspan=2, sticky='WENS')
        
        # options
        self.var = tk.StringVar(self)
        self.var.set("Select Type")
        option = tk.OptionMenu(self, self.var, *CHOICES)
        option.config(**DEFAULTS)
        option.grid(column=1, row=4, sticky='N')
        
        # button
        button = Button(self, text="Get Images", command=self.create_img_list)
        button.grid(column=2, row=4, sticky='N')
        back = Button(self, text="<--", command=self.decrese_num)
        back.grid( column=1, row=5)
        forward = Button(self, text="-->", command=self.increse_num)
        forward.grid(column=2, row=5)
        
        # set inital holding image
        init_image = "initial.jpg"
        image = Image.open(init_image)
        self.photo = ImageTk.PhotoImage(image)
        self.img_label = Label(self, image=self.photo)
        self.img_label.grid(column=1, row=6, columnspan=2, padx=5, pady=5, sticky='E')
        
    def create_img_list(self):
        sub = self.var.get()
        self.images = []
        submission = self.r.get_subreddit(sub).get_top(limit=100)
        for item in submission:
            if item.url[len(item.url)-3:] in IMG_FORMATS:
                self.images.append(item.url)
        self.get_image()
        
    def get_image(self):
        image_bytes = urlopen(self.images[self.img_num]).read()
        # internal data file
        data_stream = BytesIO(image_bytes)
        # open as a PIL image object
        image = Image.open(data_stream)
        # resize image
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)

        self.photo = tk_image = ImageTk.PhotoImage(image)

        self.img_label.config(image=tk_image)

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
    window.pack()
    root.mainloop()


