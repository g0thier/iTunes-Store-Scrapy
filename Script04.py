import json
import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#     Load .json File     #
#_________________________#

# reconstitution du chemin 
parent_dir = os.path.abspath(os.path.split(__file__)[0])
folder_name = "src"
file_name = "iTunesPages.json"

path = os.path.join(parent_dir, folder_name, file_name)

# ouverture du fichier
file = open(path)
results = json.load(file)

## Tableau sous numpy 
df = pd.DataFrame(results)

## Conversion en Liste ordonnée
list_of_lists = []

for element in results:
    list_of_lists.append( element["URL"] )

list_of_lists.sort()


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#  Import Class Function  #
#_________________________#


class QuotesSpider(scrapy.Spider):

    # Name of your spider
    name = "iTunes"

    # Url to start your spider from 
    start_urls = list_of_lists

    def parse(self, response):

        quotes = response.xpath('//*[@id="selectedcontent"]/div/ul/li')
        for quote in quotes:
            yield {
                'URL': quote.xpath('a').attrib["href"],
            }



#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
# Create Folder Directory #
#_________________________#


try: 
    parent_dir = os.path.abspath(os.path.split(__file__)[0])
    folder_name = "src"
    print(parent_dir)

    path = os.path.join(parent_dir, folder_name)
    os.mkdir(path)
except:
    print("File probably exists")


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
# Create Folder Directory #
#_________________________#


# Name of the file where the results will be saved
filename = "iTunesFilmsCollection.json"

## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.ERROR,
    "FEEDS": {
        path + '/' + filename : {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(QuotesSpider)
process.start()
