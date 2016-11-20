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

def main():

	return 0

if __name__ == '__main__':
	main()


try:
	import tkinter as tk
	from io import BytesIO
	from urllib.request import urlopen
except ImportError:
	#must be python2
	import Tkinter as tk
	from StringIO import StringIO as BytesIO
	from urllib import urlopen

from PIL import Image, ImageTk
import praw
import os

window = tk.Tk()

choices = ['pics', 'gifs', 'aww', 'EarthPorn', 'nsfw']
images = []
img_num = tk.IntVar()
basewidth = 300

def build_window():
    h = 650  # height for the Tk root
    w = 800  # width for the Tk root

    # get screen width and height
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    window.configure(background='black')
    window.title("Images 2.0")
    heading = tk.Label(window, text="IMAGES", bg="black", fg="white", font=("Courier", 44))
    intro = tk.Label(window, text="Welcome to the image generator, select your image type below.", bg="black", fg="white", font=("Courier", 12))
    # options
    global var
    var = tk.StringVar(window)
    var.set("Select Type")
    option = tk.OptionMenu(window, var, *choices)
    option.config(bg="black", fg="white")
    # button
    button = tk.Button(window, text="Get Images", command=create_img_list, bg="black", fg="white")
    back = tk.Button(window, text="<--", command=decrese_num, bg="black", fg="white")
    forward = tk.Button(window, text="-->", command=increse_num, bg="black", fg="white")

    # set inital holding image
    cwd = os.getcwd()
    init_image = cwd + "/initial.jpg"
    image = Image.open(init_image)
    photo = ImageTk.PhotoImage(image)
    img_label = tk.Label(window, image=photo, bg="black")
    tk.Label.image = photo

    # set grids
    heading.grid(column=1, row=0, rowspan=2, columnspan=2, sticky='WENS')
    intro.grid(column=1, row=2, rowspan=2, columnspan=2, sticky='WENS')
    option.grid(column=1, row=4, sticky='N')
    button.grid(column=2, row=4, sticky='N')
    back.grid( column=1, row=5)
    forward.grid(column=2, row=5)
    img_label.grid(column=1, row=6, columnspan=2, padx=5, pady=5, sticky='E')

def create_img_list():
    del images[:]
    sub = var.get()
    r = praw.Reddit(user_agent='gimmy pics')
    submission = r.get_subreddit(sub).get_top(limit=100)
    for item in submission:
        if item.url[len(item.url)-3:] == "jpg":
            images.append(item.url)
            print(item.url)
    get_image()

def get_image():
    image_bytes = urlopen(images[img_num.get()]).read()
    # internal data file
    data_stream = BytesIO(image_bytes)
    # open as a PIL image object
    image = Image.open(data_stream)
    # resize image
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)

    tk_image = ImageTk.PhotoImage(image)

    update_image(tk_image)

def update_image(tk_image):
    img_label = tk.Label(window, image=tk_image, bg="black")
    tk.Label.image = tk_image
    img_label.grid(columnspan=2, row=6, sticky='E', padx=5, pady=5)

def increse_num():
    img_num.set(img_num.get() + 1)
    get_image()

def decrese_num():
    img_num.set(img_num.get() - 1)
    get_image()

build_window()

window.mainloop()
