# -*- coding: utf-8 -*-


"""
   This Spider user to scrape vedios by search keyword.

   This file  contains the following functions:

        * __init__ - to overwrite original class paramters.
        * start_requests - start scrapy request and call parse for every vedio url.
        * parse - parsing vedio info.

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



class ScrapeBySearch(Spider):

    name = 'YTSearch'
    allowed_domians = ['www.youtube.com']
    page = 1

    def __init__(self, KeyWord=None,  *args, **kwargs):
        super(ScrapeBySearch, self).__init__(*args, **kwargs)

        self.KeyWord = KeyWord
        self.start_url  = "https://www.youtube.com/results?search_query=%s"  % KeyWord

    def start_requests(self):
        if self.KeyWord == None:
            CloseSpider("Please enter a valid keyword")
        yield scrapy.Request(self.start_url, self.parse)



    def parse(self, response):
        results = response.css('.item-section').xpath('li')

        for result in results:
            try:
                Link = result.css("div.yt-lockup-thumbnail.contains-addto a.yt-uix-sessionlink.spf-link").attrib['href']
                Link = "https://www.youtube.com/" + Link
                yield scrapy.Request(Link, self.video_info)      
            except:
                print('error')
                url = ''

        next_pages = response.css('.branded-page-box > a')
        i = 0
        for page in next_pages:
            i += 0
            try:
                next_page = page.attrib['href']
                print("nEXt",next_page)
                url = 'https://www.youtube.com' + next_page
                print(next_page)
                yield scrapy.Request(url, self.parse)
            except:
                print("next error")
                pass

            if i >= 6: # if next page button appear recount pages
                next_pages = response.css('.branded-page-box > a')

            yield scrapy.Request(url, self.parse)




    def video_info(self, response):
        url = response.url
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


        yield{ # look at pipeline file for more info about database
            'spider': 'YTSearch',
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
            'KeyWord':str( self.KeyWord),
            "VideoLink": str(url),
            'ChannelLink': str(channelLink)
            }