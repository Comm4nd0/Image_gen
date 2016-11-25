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
import browser

CHOICES = ['pics', 'gifs', 'aww', 'EarthPorn', 'funny', 'instant_regret', 'nsfw']
IMG_FORMATS = ['.jpg', '.png', '.jpeg', '.bmp']
GIF = []
TITLE = []

class ImageGetter(praw.Reddit):
    def load_subreddit(self, subreddit):
        #makes the generator. Reddit has a limit of 1,000 results
        self.images = []
        self.subreddit = self.get_subreddit(subreddit).get_hot(limit=None)
        del TITLE[:]

    def get_img_url(self, num=None):
        """returns the image url from the list or the next image in the subreddit"""
        global TITLE
        if num is None or num >= len(self.images):
            for item in self.subreddit:
                if os.path.splitext(item.url)[1] in IMG_FORMATS:
                    TITLE.append(item.title)
                    self.images.append(item.url)
                    return item.url
        else:
            return self.images[num]

    def get_img_title(self, title):
        return title


class GUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.center(1000, 850)
        self.master.configure(background='black')
        self.master.title("Images 2.0")

        # causes the full width of the window to be used
        self.columnconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        self.make_UI()
        self.r = ImageGetter(user_agent='gimmy pics')
        self.img_num = 0

        self.web = browser.createWebpage()

    def make_UI(self):
        style = ttk.Style()
        # global style changes
        style.configure(".", background='black', foreground='grey', anchor="center")
        # Button style changes
        style.map("TButton", background=[('hover', 'blue')])
        # Optionmenu. The actual menu cannot be themed :(
        style.map("TMenubutton", background=[('hover', 'blue')])
        style.map("TEntry", foreground=[('focus', 'blue2')])
        style.map("TEntry", foreground=[('active', 'green2')])

        heading = ttk.Label(self, text="IMAGES", font=("Courier", 44))
        heading.grid(column=0, row=0, rowspan=2, columnspan=4, sticky='WENS')

        intro = ttk.Label(self, font=("Courier", 16))
        intro['text']="Welcome to the image generator, select your image type below."
        intro.grid(column=0, row=2, rowspan=2, columnspan=4, sticky='WENS', padx=5, pady=20)

        # EXIT
        exit_button = ttk.Button(self, text="Exit", command=self.exit)
        exit_button.grid(column=0, row=0, sticky='NW')

        # free text label
        free_text = ttk.Label(self, font=("Courier", 12))
        free_text['text'] = "Manual entry"
        free_text.grid(column=0, row=4, sticky='E', padx=5, pady=5)

        # drop down label
        drop_down_text = ttk.Label(self, font=("Courier", 12))
        drop_down_text['text'] = "or drop down menu"
        drop_down_text.grid(column=0, row=5, sticky='E', padx=5, pady=5)

        # options
        self.var = tk.StringVar(self)
        self.var.set("Select Type")
        option = ttk.OptionMenu(self, self.var, "Select Subreddit", *CHOICES)
        option.grid(column=1, row=5, sticky='WENS', padx=5, pady=5)

        # free text box
        self.text = ttk.Entry(self)
        self.text.grid(column=1, row=4, sticky='WENS', padx=5, pady=5)

        # button
        button = ttk.Button(self, text="Get Images", command=self.create_img_list)
        button.grid(column=2, row=4, sticky='WENS', padx=5, pady=5)

        # navigation buttons
        back = ttk.Button(self, text="<--", command=self.decrese_num)
        back.grid( column=2, row=5, sticky='WENS', padx=5, pady=5)
        forward = ttk.Button(self, text="-->", command=self.increse_num)
        forward.grid(column=3, row=5, sticky='WENS', padx=5, pady=5)

        # side panel buttons
        browser_button = ttk.Button(self, text="Open in Browser", command=self.load_browser)
        browser_button.grid(column=3, row=4, sticky='WENS', padx=5, pady=5)

        # set initial title
        self.img_title = ttk.Label(self, font=("Courier", 15), wraplength=750)
        self.img_title['text'] = "Minions"
        self.img_title.grid(column=0, row=6, rowspan=2, columnspan=4, sticky='NSEW', padx=5, pady=5)

        # set inital holding image
        init_image = "initial.jpg"
        image = Image.open(init_image)
        self.photo = ImageTk.PhotoImage(image)
        self.img_label = ttk.Label(self, image=self.photo)
        self.img_label.grid(column=0, row=8, columnspan=4, padx=5, pady=5)

        self.master.bind("<Return>", self.bind_handler)

    def get_title(self):
        self.img_title['text'] = TITLE[self.img_num]

    def bind_handler(self, idk):
        self.create_img_list()

    def create_img_list(self):
        #free_text = self.text.get()
        if len(self.text.get()) > 0:
            sub = self.text.get()
            self.r.load_subreddit(sub)
        else:
            self.r.load_subreddit(self.var.get())
        self.img_num = 0
        self.get_image()

    def get_image(self):
        try:
            image_bytes = urlopen(self.r.get_img_url(self.img_num)).read()
        except:
            self.no_images()
        # internal data file
        data_stream = BytesIO(image_bytes)
        # open as a PIL image object
        image = Image.open(data_stream)
        # resize image
        width = self.winfo_width() - 500
        wpercent = (width / float(image.size[0]))
        hsize = int((float(image.size[1] ) * float(wpercent)))
        image = image.resize((width, hsize), Image.ANTIALIAS)

        self.photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=self.photo)
        self.get_title()

    def load_browser(self):
        # load images and webpage
        res = self.web.get_urls(self.var.get())

        # if none found then show empty image
        if res == 0:
            self.no_images()
        elif res == 1:
            self.img_title['text'] = "Web page loaded! Have fun ;)"
            self.path = os.getcwd() + "/browser.jpg"
            image = Image.open(self.path)
            self.photo = ImageTk.PhotoImage(image)
            self.img_label.config(image=self.photo)

    def no_images(self):
        self.img_title['text'] = "No images found! :'("
        self.path = os.getcwd() + "/empty.jpeg"
        image = Image.open(self.path)
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
    def exit(self):
        quit()


if __name__ == '__main__':
    root = tk.Tk()
    window = GUI(root)
    window.pack(fill=tk.X, expand=True, anchor=tk.N)
    root.mainloop()

