# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3 as sql
from scrapy.conf import settings


class YoutubescrapePipeline(object):
    def process_item(self, item, spider):
        return item

# every spider has it's own pipeline and database setting
#because the data stracture id different
class SqLitePipeline(object):

    def __init__(self):
        self.connection = sql.connect(settings['SQL_DB'])
        self.cursor = self.connection.cursor()

    def create_table(self, cursor, connection,name):
        # create table if not exits
        if name == 'Search': # if spider is channel spider
            try:
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {settings['SQL_TABLE'][0]}(VedioName TEXT,Tags TEXT,ChannelName TEXT, \
                                    ChannelVerification TEXT, Views TEXT, Likes TEXT,Dislikes TEXT,UploadTime TEXT,\
                                    Discription TEXT ,ExtraInfo TEXT, KeyWord TEXT, ChannelLink TEXT, VideoLink TEXT)")

                self.cursor.execute("CREATE INDEX fast_VedioName ON Search(VedioName)")
                self.cursor.execute("CREATE INDEX fast_Tags ON Search(Tags)")
                self.cursor.execute("CREATE INDEX fast_ChannelName ON Search(ChannelName)")
                self.cursor.execute("CREATE INDEX fast_ChannelVerification ON Search(ChannelVerification)")
                self.cursor.execute("CREATE INDEX fast_Views ON Search(Views)")
                self.cursor.execute("CREATE INDEX fast_Likes Search(Likes)")
                self.cursor.execute("CREATE INDEX fast_Dislikes Search(Dislikes)")
                self.cursor.execute("CREATE INDEX fast_UploadTime Search(UploadTime)")
                self.cursor.execute("CREATE INDEX fast_DiscriptionText Search(Discription)")
                self.cursor.execute("CREATE INDEX fast_ExtraInfo Search(ExtraInfo)")
                self.cursor.execute("CREATE INDEX fast_KeyWord Search(KeyWord)")
                self.cursor.execute("CREATE INDEX fast_ChannelLink Search(ChannelLink)")
                self.cursor.execute("CREATE INDEX fast_VideoLink Search(VideoLink)")
                self.connection.commit()
                # print('DOne')
            except Exception as e:
                print(str(e))

        # if spider is channel spider
        elif name == 'channel': 
            print("ceate")
            try:
                print(settings['SQL_TABLE'][1])
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {settings['SQL_TABLE'][1]}(ChannelName TEXT,subscriptionCount TEXT,Views TEXT, joineDate TEXT, socialLinks TEXT, VideoCount TEXT")

                self.cursor.execute("CREATE INDEX fast_ChannelName ON Channel(ChannelName)")
                self.cursor.execute("CREATE INDEX fast_subscriptionCount ON Channel(subscriptionCount)")
                self.cursor.execute("CREATE INDEX fast_Views ON Channel(Views)")
                self.cursor.execute("CREATE INDEX fast_joineDate ON Channel(joineDate)")
                self.cursor.execute("CREATE INDEX fast_socialLinks ON Channel(socialLinks)")
                self.cursor.execute("CREATE INDEX fast_VideoCount Channel(VideoCount)")
                self.connection.commit()
                print('DOne')
            except Exception as e:
                print(str(e))



    def process_item(self, item, spider):

        if spider.name == 'YTSearch': # for search by keyword spider
            # self.create_table(self.cursor, self.connection, name='Search' )
            self.cursor.execute("INSERT INTO Search(VedioName ,Tags ,ChannelName ,ChannelVerification , Views , Likes , \
                        Dislikes ,UploadTime ,Discription ,ExtraInfo ,KeyWord , ChannelLink,VideoLink) VALUES (?, ?,?, ?,?, ?, ?,?, ?, ?,?, ?,?)",
                        (item['VedioName'],item['Tags'], item['ChannelName'], item['ChannelVerification'], item['Views'], item['Likes'],
                        item['Dislikes'], item['UploadTime'], item['Discription'], item['ExtraInfo'], item['KeyWord'], item['ChannelLink'],
                        item['VideoLink'],))
            self.connection.commit()
            return item
        
        elif spider.name == 'YTChannel': # for channel spider
            print("in channel")
            # self.create_table( self.cursor, self.connection,name='channel')
            print('insert')
            self.cursor.execute("INSERT INTO Channel(ChannelName ,subscriptionCount ,Views ,joineDate , socialLinks ) VALUES (?,?, ?,?, ?)",
                        (item['ChannelName'],item['subscriptionCount'], item['Views'], item['joineDate'], item['socialLinks'],))
            self.connection.commit()
            return item
