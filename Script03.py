import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#      Load txt File      #
#_________________________#


# reconstitution du chemin 
parent_dir = os.path.abspath(os.path.split(__file__)[0])
folder_name = "src"
file_name = "url_list.txt"

path = os.path.join(parent_dir, folder_name, file_name)

# reconstitution de la liste
my_file = open(path, "r")
content = my_file.read()
content_list = content.split("\n")[:-1]

print(content_list)


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#  Import Class Function  #
#_________________________#


class QuotesSpider(scrapy.Spider):

    # Name of your spider
    name = "iTunes"

    # Url to start your spider from 
    start_urls = content_list

    def parse(self, response):

        # [1]/a
        # //*[@id="selectedgenre"]/ul[2]/li[2]/a
        quotes = response.xpath('//*[@id="selectedgenre"]/ul[2]/li')
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
filename = "iTunesPages.json"

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