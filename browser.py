#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Documentation is like sex.
#   Code for created a webpage slider viwing all the anamated stuff!

import os
import praw
import webbrowser

ANA_FORMAT = ['.mp4', '.webm']

class createWebpage():
    def __init__(self):
        self.image_paths = []
        self.image_urls = ""
        self.web = praw.Reddit(user_agent='gimmy ana_pics')
        del self.image_paths[:]

    def get_urls(self, subreddit):
        self.subreddit = self.web.get_subreddit(subreddit).get_hot(limit=100)
        for item in self.subreddit:
            if os.path.splitext(item.url)[1] in ANA_FORMAT:
                self.image_paths.append(item.url)
                print(item.url)
        print(len(self.image_paths))
        self.makeHTML()

    def makeHTML(self):
        for url in self.image_paths:
            type = os.path.splitext(url)[1]
            type = type.replace('.', '')
            self.image_urls += '<source src="' + url + '" type="video/' + type + '">'
            print(self.image_urls)


        self.html = """<!DOCTYPE html>
        <html>
        <title>Images </title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://www.w3schools.com/lib/w3.css">
        <body>

        <h2 class="w3-center">Anamated Images</h2>

        <div class="w3-content w3-display-container">
        <video autoplay
        """

        self.html += self.image_urls

        self.html += """
        </video>
          <a class="w3-btn-floating w3-display-left" onclick="plusDivs(-1)">&#10094;</a>
          <a class="w3-btn-floating w3-display-right" onclick="plusDivs(1)">&#10095;</a>
        </div>

        <script>
        var slideIndex = 1;
        showDivs(slideIndex);

        function plusDivs(n) {
          showDivs(slideIndex += n);
        }

        function showDivs(n) {
          var i;
          var x = document.getElementsByClassName("mySlides");
          if (n > x.length) {slideIndex = 1}
          if (n < 1) {slideIndex = x.length}
          for (i = 0; i < x.length; i++) {
             x[i].style.display = "none";
          }
          x[slideIndex-1].style.display = "block";
        }
        </script>

        </body>
        </html>"""
        with open('images.html', 'w') as webpage:
            webpage.write(self.html)
            webpage.close()
        self.loadBrowser()

    def loadBrowser(self):
        webbrowser.open('images.html')
