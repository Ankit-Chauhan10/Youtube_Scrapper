"""
   This Spider user to scrape youtube spacific vedio comments

   This file  contains the following functions:

        * __init__ - to overwrite original class paramters.
        * start_requests - start headless seleinum request.
        * parse_page - parsing vedio comments.

    example to call spider from cmd:
    > scrapy crawl YTComment -a VedioUrl= https://www.youtube.com/watch?v=_uQrJ0TkZlc


    for more info about scrapy-selenium visit: 
        https://github.com/clemfromspace/scrapy-selenium
        
"""

from selenium.webdriver.common.keys import Keys
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from scrapy import Selector
from scrapy import Spider
import scrapy
import time


class ScrapeComment(Spider):
    name = 'YTComment'  # spider name
   

    def __init__(self, VedioUrl='',  *args, **kwargs):
        super(ScrapeComment, self).__init__(*args, **kwargs)
        self.start_url  = VedioUrl # vedio link


    def start_requests(self):

        yield SeleniumRequest( # start selenuim request
        url=self.start_url, 
        callback=self.parse_page,
        )

    def parse_page(self, response):

        driver = response.request.meta['driver']
        response =Selector(text=driver.page_source) # get the current driver status source
        time.sleep(2) # wait until page loading
     
        driver.execute_script("window.scrollTo(0, 10000);") # scroll down to reach commentd
        time.sleep(5)
        sel =Selector(text=driver.page_source)

        try:
            N_of_comments = sel.xpath('//*[@id="count"]/yt-formatted-string/text()').get().split(' ')[0] # number of comments
        except:
            driver.execute_script("window.scrollTo(0, 1000);")
            time.sleep(2)
            sel =Selector(text=driver.page_source)
            N_of_comments = sel.xpath('//*[@id="count"]/yt-formatted-string/text()').get().split(' ')[0]

        N_of_comments = int(''.join(N_of_comments.split(','))) # split number from word comment
        print("COUNT",N_of_comments)

        comments = sel.xpath('//*[@id="comment"]') # number of loaded comments
        print(len(comments))


        if len(comments) >= 0:
            for comment in comments:
                CommentAuther = comment.css("#author-text > span ::text").get()
                commentDate = comment.css("#header-author > yt-formatted-string > a ::text").get()
                Text = " ".join(comment.css("#content-text ::text").getall())
                Likes = " ".join(comment.css("#vote-count-middle ::text").getall())  
                # print(CommentAuther)

                yield{
                    'CommentAuther' :CommentAuther,
                    'commentDate': commentDate,
                    'Text':Text,
                    'Likes':Likes
                    }
              