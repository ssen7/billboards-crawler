# billboards-crawler
## TO RUN the crawler follow these steps:
1. Using the Terminal or Anaconda Prompt.
2. git clone this repository.
3. cd billboards_crawler
4. Run the following : ‘scrapy crawl billboards -a nweeks=100 -a base_date=2018-07-28 -a timedelta=7 -a save_dir='./billboard_data’
   1. Note: the arguments are optional, shown are the default values. Just use 'scrapy crawl billboards' to use defaults
5. Check the CSV files generated in the save directory.
