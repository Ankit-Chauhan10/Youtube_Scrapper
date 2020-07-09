# -*- coding: utf-8 -*-

"""
   This Spider user to scrape youtube spacific channel.

   This file  contains the following functions:

        * __init__ - to overwrite original class paramters.
        * start_requests - start headless seleinum request.
        * channel_about - parsing vedio about section.

    example to call spider from cmd:
    > scrapy crawl YTChannel -a ChannelUrl= channelUrl


    for more info about scrapy-selenium visit: 
        https://github.com/clemfromspace/scrapy-selenium
        
"""

from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
import scrapy


class ScrapeComment(Spider):

    name = 'YTChannel'
    allowed_domians = ['www.youtube.com']




    def __init__(self, ChannelUrl='',  *args, **kwargs):
        super(ScrapeComment, self).__init__(*args, **kwargs)
        self.start_url  = ChannelUrl + "/about" # channel link + about to goto about section

    def start_requests(self):
        if self.start_url == None or self.start_url == '':
            CloseSpider("Please enter a valid vedio Link")
        yield scrapy.Request(self.start_url, self.channel_about)




    def channel_about(self, response):
        ChannelName = response.css(".branded-page-header-title-link ::text").get()
        subscriptionCount = response.css("span.about-stat:nth-child(1) ::text").get()
        Views = "".join(response.css("span.about-stat:nth-child(2) > b:nth-child(1) ::text").getall())
        joineDate = response.css("span.about-stat:nth-child(4) ::text").get()
        link1 = response.css("ul.about-custom-links:nth-child(2) > li:nth-child(1) > a:nth-child(1)").attrib['href']
        link2 = response.css(".about-secondary-links > li:nth-child(1) > a:nth-child(1)").attrib['href']
        link3 = response.css(".about-secondary-links > li:nth-child(2) > a:nth-child(1)").attrib['href']
        socialLinks = ', '.join([link1, link2, link3])

 

        yield{
            'ChannelName' :str(ChannelName),
            'subscriptionCount': str(subscriptionCount),
            'Views':str(Views),
            'joineDate':str(joineDate),
            'socialLinks':str(socialLinks)
            }




    # def video_count(self, response):
    #     data = ChannelItems()
    #     try:
    #         count = response.css("div.yt-lockup-meta:nth-child(2) > ul:nth-child(1) > li:nth-child(1) ::text").get()
    #     except:
    #         count = ''
    #     data['ChannelName'] = count
    #     yield data





    # def channel_videos(self, response):
    #     driver = response.request.meta['driver']
    #     # while True:
    #     #     driver.execute_script("window.scrollTo(0, 1000);")
    #     #     time.sleep(5)
    #     #     sel =Selector(text=driver.page_source)
    #     #     items = sel.css("#items > ytd-grid-video-renderer")
    #     #     print(len(items))
    #     html = driver.find_element_by_tag_name('html')
    #     html.send_keys(Keys.END)
    #     time.sleep(10)
    #     sel =Selector(text=driver.page_source)
    #     items = sel.css("#items > ytd-grid-video-renderer")
    #     print(len(items))
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(5)
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(5)
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(5)
    #     sel =Selector(text=driver.page_source)
    #     items = sel.css("#items > ytd-grid-video-renderer")
    #     print(len(items))
    #     try:
    #         button = driver.find_element_by_css_selector(".load-more-button")
    #         back.click()
    #     except:
    #         print("Npone")
    #     sel =Selector(text=driver.page_source)
    #     items = sel.css("#items > ytd-grid-video-renderer")
    #     print(len(items))
    #     # sel =Selector(text=driver.page_source)
    #     # items = sel.css("#channels-browse-content-grid >li")
    #     # print(len(items))
    #     # print(driver)
    #     response.css("div.yt-lockup-meta:nth-child(2) > ul:nth-child(1) > li:nth-child(1) ::text").get()