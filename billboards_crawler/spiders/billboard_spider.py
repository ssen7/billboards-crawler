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

# create subclass of Scrapy Spider
class BillBoardCrawler(scrapy.Spider):
    
    # Name of the Spider
    name="billboards"
    
    # Give a time delay of 1.25s for each GET request
    custom_settings = {
        'DOWNLOAD_DELAY' : '1.25' 
    }

    # create start requests
    def start_requests(self):
        
        # create base URL
        base_url = 'https://www.billboard.com/charts/hot-100/'
        
        # Create starting date
        basedate = datetime.datetime.strptime('2018-07-28','%Y-%m-%d')
        
        dateList = []
        urlList = []
        
        numOfWeeks = 500

        # Generate end dates of each week
        for i in range(numOfWeeks):
            basedate = basedate - datetime.timedelta(days=7);
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
        
        # Initialize Lists for Song Names, Artist and Rank
        nameList = []
        artistList = []
        rankList = ['1']
        
        # Get the First Ranked Song details 
        oneName = soup.find('div', attrs={'class':'chart-number-one__title'})
        oneArtist = soup.find('div', attrs={'class':'chart-number-one__artist'})
        oneArtist = oneArtist.a.text if oneArtist.a != None else oneArtist.text
        
        nameList.append(oneName.text)
        artistList.append(oneArtist.strip())
        
        # Get the song data
        songs = soup.find_all('div', attrs={'class':'chart-list-item'})
        for song in songs:
            
            songName = song['data-title']
            artistName = song['data-artist']
            rank = song['data-rank']
            
            nameList.append(songName)
            artistList.append(artistName)
            rankList.append(rank)
        
        # Generate Datasets for each week
        songNameSr = pd.Series(nameList)
        artistNameSr = pd.Series(artistList)
        rankSr = pd.Series(rankList)
        csvYear= response.url.split("/")[-1]
        date = [csvYear]*100
        dateSr = pd.Series(date)
        
        finalDF = pd.DataFrame(songNameSr, columns=['song'])
        finalDF['artist'] = artistNameSr
        finalDF['rank'] = rankSr
        finalDF['week'] = dateSr
        
        # write to CSV file
        filename = 'billboard-%s.csv' % csvYear
        
        finalDF.to_csv(filename)