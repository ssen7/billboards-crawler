# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 13:13:35 2018

Homework Name: Homework3 (Python web crawler/scraper)
Names: Navin Kasa (nk4xf), Saurav Sengupta (ss4yd)
Computing ID : nk4xf, ss4yd
"""
# import relevant packages
import scrapy
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import os


# create subclass of Scrapy Spider
class BillBoardCrawler(scrapy.Spider):

    # Name of the Spider
    name = "billboards"

    # Give a time delay of 1.25s for each GET request
    custom_settings = {
        'DOWNLOAD_DELAY': '1.25'
    }

    def __init__(self, nweeks=100, base_date=date.today(), timedelta=7, save_dir='./billboard_data', *args, **kwargs):
        super(BillBoardCrawler, self).__init__(*args, **kwargs)
        super().__init__(**kwargs)
        self.nweeks = int(nweeks)
        self.base_date = base_date
        self.timedelta = timedelta
        self.save_dir = save_dir

    # create start requests
    def start_requests(self):

        # create base URL
        base_url = 'https://www.billboard.com/charts/hot-100/'

        # Create starting date
        # basedate = datetime.datetime.strptime('2018-07-28', '%Y-%m-%d')
        basedate = self.base_date

        dateList = []
        urlList = []

        numOfWeeks = self.nweeks

        # Generate end dates of each week
        for i in range(numOfWeeks):
            basedate = basedate - datetime.timedelta(days=self.timedelta)
            str_date = basedate.strftime('%Y-%m-%d')
            dateList.append(str_date)

        # Append each date to base URL to generate unique URL List
        for date in dateList:
            url = base_url + date
            urlList.append(url)

        # Make requests asynchronously, on callback reference the parse method
        for url in urlList:
            yield scrapy.Request(url=url, callback=self.parse)

    # Method to parse incoming HTML data and convert to relevant CSV files
    def parse(self, response):

        # Get HTML body from response
        page = response.body

        # Use Beautiful Soup to parse HTML
        soup = BeautifulSoup(page, 'html.parser')

        song_name_tag = 'chart-element__information__song'
        artist_name_tag = 'chart-element__information__artist'
        default_tag = 'chart-element__information__delta__text text--default'
        last_week_tag = 'chart-element__meta text--center color--secondary text--last'
        peak_rank_tag = 'chart-element__meta text--center color--secondary text--peak'
        week_chart_tag = 'chart-element__meta text--center color--secondary text--week'
        # album_art_tag='chart-element__image flex--no-shrink'

        song_names = [x.get_text()
                      for x in soup.find_all('span', song_name_tag)]
        artist_names = [x.get_text()
                        for x in soup.find_all('span', artist_name_tag)]
        default = [x.get_text()
                   for x in soup.find_all('span', default_tag)]
        last_week = [x.get_text()
                     for x in soup.find_all('span', last_week_tag)]

        peak_rank = [x.get_text()
                     for x in soup.find_all('span', peak_rank_tag)]
        week_chart = [x.get_text()
                      for x in soup.find_all('span', week_chart_tag)]

        # save to dataframe
        df = pd.DataFrame()
        df['rank'] = list(range(1, 101))
        df['song_name'] = song_names
        df['artist_name'] = artist_names
        df['default'] = default
        df['last_week'] = last_week
        df['peak_rank'] = peak_rank
        df['week_chart'] = week_chart

        # create save directory
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        csvYear = response.url.split("/")[-1]
        filename = os.path.join(self.save_dir, 'billboard-%s.csv' % csvYear)

        # save to dir
        df.to_csv(filename, index=False)
