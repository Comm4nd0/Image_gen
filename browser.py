#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Documentation is like sex.
#   Code for created a webpage slider viwing all the anamated stuff!

import os
import praw
import webbrowser
import urllib3

from bs4 import BeautifulSoup

ANA_FORMAT = ['.mp4', '.webm', '.gifv', '.jpg', '.png', '.jpeg', '.bmp']


class createWebpage():
    def __init__(self):
        self.image_paths = []
        self.image_html = ""
        self.img_thumbnails = []
        self.web = praw.Reddit(user_agent='gimmy ana_pics')
        self.http = urllib3.PoolManager()

    def get_urls(self, sub):
        del self.image_paths[:]
        del self.img_thumbnails[:]
        self.sub = sub

        self.subreddit = self.web.get_subreddit(self.sub).get_hot(limit=100)
        # test to see if sub_res has any content
        try:
            for test in self.subreddit:
                test = test.title
                print(test)
                if len(test) > 0:
                    break
                else:
                    break
        except:
            self.subreddit = self.web.search(self.sub, limit=100)

        for item in self.subreddit:
            if os.path.splitext(item.url)[1] in ANA_FORMAT:
                self.image_paths.append(item.url)
                self.img_thumbnails.append(item.thumbnail)
            elif 'gfycat.com' in item.url:
                self.get_gfycat(item.url)
                self.img_thumbnails.append(item.thumbnail)

        self.makeHTML()
        return 1

    def makeHTML(self):
        num = 0
        self.image_html = ""
        for url in self.image_paths:
            self.image_html += '<a href="' + url + '" data-poster="' + self.img_thumbnails[num] + '" data-webm="' + url + '"><img src="' + self.img_thumbnails[num] + '"  width="250px" height="250px"></a>'
            num += 1

        self.html = """<!DOCTYPE html>
        <html><head><script type="text/javascript" id="www-widgetapi-script" src="test_files/www-widgetapi.js" async=""></script>
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="width=device-width">
            <title>Image gallery</title>



        <body>
        <h1>IMAGE GEN - """
        self.html += self.sub

        self.html += """</h1>
        <a href="initial.jpg" style="display: none;"><img src="initial.jpg" alt="Waves" data-description="Minions!"></a>
        """

        self.html += self.image_html

        self.html += """
        <a href="initial.jpg" style="display: none;"><img src="initial.jpg" alt="Waves" data-description="Minions!"></a>
        </body></html>
        """
        with open('images.html', 'w') as webpage:
            webpage.write(self.html)
            webpage.close()
        self.loadBrowser()

    def loadBrowser(self):
        webbrowser.open('images.html')

    def get_gfycat(self, url):
        try:
            req = self.http.request('GET', url)
            soup = BeautifulSoup(req.data, "lxml")
            scrape = soup.find_all(id="mp4Source")
            scrape = str(scrape[0])
            start = scrape.find('https://')
            end = scrape.find('.mp4') + 4
            self.image_paths.append(scrape[start:end])
        except:
            pass
