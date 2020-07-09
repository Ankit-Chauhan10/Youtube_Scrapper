# -*- coding: utf-8 -*-

"""
   This Spider user to scrape youtube vedio info

   This file  contains the following functions:

        * __init__ - to overwrite original class paramters.
        * start_requests - start scrapy request
        * video_info - parsing vedio info.

    example to call spider from cmd:
    > scrapy crawl YTVedio -a VedioUrl= https://www.youtube.com/watch?v=_uQrJ0TkZlc


    for more info about scrapy: 
        https://doc.scrapy.org/en/latest/topics/selectors.html
        
"""


from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
import scrapy



class ScrapeByVedio(Spider):

    name = 'YTVedio' # spider name
    allowed_domians = ['www.youtube.com']

    def __init__(self, VedioUrl=None,  *args, **kwargs):
        super(ScrapeByVedio, self).__init__(*args, **kwargs)
        self.url = VedioUrl
        self.start_url  = self.url

    def start_requests(self):
        if self.url == None or self.url == '':
            CloseSpider("Please enter a valid vedio Link")
        yield scrapy.Request(self.start_url, self.video_info) 

    
    def video_info(self, response):
        vedio_name = response.xpath('//*[@id="eow-title"]/text()').get()
        tags = ", ".join(response.css(".standalone-collection-badge-renderer-text ::text").getall())
        channelName = ", ".join(response.css('.yt-user-info > a:nth-child(1) ::text').getall())
        channelLink = response.css('.yt-user-info > a:nth-child(1)').attrib['href']
        try:
            ChannelVerification = response.css('.yt-channel-title-icon-verified').attrib['data-tooltip-text']
        except:
            ChannelVerification = ''
        views =  response.css('.watch-view-count ::text').get()
        likes = response.css('.like-button-renderer-like-button-unclicked > span:nth-child(1) ::text').get()
        dislikes =  response.css('.like-button-renderer-dislike-button-unclicked > span:nth-child(1)  ::text').get()
        uploadTime = response.css('.watch-time-text  ::text').get()
        discription = ', '.join(response.css('#watch-description-text ::text').getall())
        extraInfo = ', '.join(response.css('.watch-extras-section ::text').getall())
        

        # yield data to be saved in database
        yield{
            'VedioName' :str(vedio_name),
            'Tags': str(tags),
            'ChannelName':str(channelName),
            'ChannelVerification':str(ChannelVerification),
            'Views':str(views),
            'Likes':str(likes),
            'Dislikes':str(dislikes),
            'UploadTime':str(uploadTime),
            'Discription':str(discription),
            'ExtraInfo': str(extraInfo),
            'KeyWord':str(self.start_url),
            "VideoLink": str(self.start_url),
            'ChannelLink': str(channelLink)
            }