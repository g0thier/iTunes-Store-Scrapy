import json
import logging
import os
from turtle import title
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest

# Intall for delay and rotation proxy
# pip install scrapy-user-agents
# pip install scrapy-rotating-proxies
# pip install rotating-free-proxies

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#     Load .json File     #
#_________________________#
print("Load .json File...")

# reconstitution du chemin 
parent_dir = os.path.abspath(os.path.split(__file__)[0])
folder_name = "src"
file_name = "iTunesFilmsCollection.json"

path = os.path.join(parent_dir, folder_name, file_name)

# ouverture du fichier
file = open(path)
results = json.load(file)

## Conversion en Liste ordonnée
list_of_lists = []

for element in results:
    list_of_lists.append( element["URL"] )

list_of_lists.sort()

print("...Load .json File")
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#  Import Class Function  #
#_________________________#
print("Import Class Function...")

class QuotesSpider(scrapy.Spider):

    # Name of your spider
    name = "iTunes"
    
    # Url to start your spider from 
    start_urls = list_of_lists[:20]

    # Delay for don't be desallow 
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True, # limite pour ménager les serveur 
        'AUTOTHROTTLE_DEBUG': True, # affiche le debug
        'DOWNLOAD_DELAY': 0.2, # temps entre les requetes 
        'DEPTH_LIMIT': 1, # profondeur de recherche 
    }

    
    # Rotation de proxy 
    ROTATING_PROXY_LIST_PATH = '/my/path/proxies.txt' # Path that this library uses to store list of proxies
    NUMBER_OF_PROXIES_TO_FETCH = 5 # Controls how many proxies to use

    # paralelle
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        #'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        #'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        'rotating_free_proxies.middlewares.RotatingProxyMiddleware': 610,
        'rotating_free_proxies.middlewares.BanDetectionMiddleware': 620,
    }

    # Recherche Requête 
    def parse(self, response):

        print('HTTP status normal 200 :')
        print(response.status)

        quotes = response.xpath("//*[@class='animation-wrapper is-visible']")

        for quote in quotes:
            
            # Requete 
            urlMo = response.url

            title = quote.xpath('section[1]/div[2]/div[2]/div[1]/div[2]/header/h1/text()').get() #OK
            resum = quote.xpath('section[1]/div[2]/div[2]/div[1]/div[2]/header/div[1]/section/div').getall() #OK
            creat = quote.xpath('section[1]/div[2]/div[2]/div[1]/div[2]/header/ul[2]/li[1]/ul/li[3]/time').attrib["datetime"] #OK
            durat = quote.xpath('section[1]/div[2]/div[2]/div[1]/div[2]/header/ul[2]/li[1]/ul/li[2]/text()').get() #OK

            categ = quote.xpath('section[1]/div[2]/div[2]/div[1]/div[2]/header/ul[2]/li[1]/ul/li[1]/a/text()').get() #OK
            caURL = quote.xpath('section[1]/div[2]/div[2]/div[1]/div[2]/header/ul[2]/li[1]/ul/li[1]/a').attrib["href"] #OK

            artwo = quote.xpath('section[1]/div[2]/div[1]').getall() #OK
            pegiM = quote.xpath('section[1]/div[2]/div[2]/div[1]/div[2]/header/ul[1]/li').getall() #OK
            price = quote.xpath('section[1]/div[2]/div[2]/div[1]/div[2]/header/ul[3]/li/ul').getall() #OK

            trail = quote.xpath('section[2]/div[2]/div/div[1]/div/button').getall()

            squad = response.xpath("//*[@class='cast-list__detail']").getall() #OK

            sect3 = quote.xpath('div[2]/div').getall() # <---------- Informations / Langues / Accessibilité

            music = quote.xpath('section[4]/div[2]').getall() #OK


            #¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
            #     Transformations     #
            #_________________________#     

            try:
                resum = re.search('data-test-bidi>(.*?)</p>', resum[0]).group(1)
            except:
                resum = ""

            try:
                durat = int(re.search('(.*?)heure', durat).group(1))*60 + int(re.search('heure(.*?)minutes', durat).group(1))
            except:
                durat = 0

            try:
                artworks_URLs = re.search('<source srcset="(.*?)type="image/jpeg">', artwo[0]).group(1)
                artworks_URLs = re.findall(r'(https?://[^\s]+)', artworks_URLs)
            except:
                artworks_URLs = []

            pegiM = str( pegiM[0].replace('\n','') )
            for i in range(10):
                pegiM = pegiM.replace('  ',' ')

            badges = re.search('<ul class="inline-list inline-list--content-badges">(.*?)</ul>', pegiM).group(1)
            badges = re.findall('badge-asset--(.*?)">', badges)
            
            try:
                pegi_info = re.search('Common Sense Age </span>(.*?)</li>', pegiM).group(1)
            except:
                pegi_info = ""

            rent_movie = float( re.search('Louer(.*?)€', price[0]).group(1).replace(',','.') )

            buy_movie = float( re.search('Acheter(.*?)€', price[0]).group(1).replace(',','.') )

            sect3 = str( sect3[0].replace('\n','') )
            for i in range(10):
                sect3 = sect3.replace('  ',' ')

            try:
                studio = re.search('Studio </dt> <dd class="information-list__item__definition">(.+?)</dd>', sect3).group(1)
            except:
                studio = ""

            try:
                copyright = re.search('definition--copyright">(.+?)</dd>', sect3).group(1)
            except:
                copyright = ""
            
            try:
                primary_lang = re.search('Principale </dt> <dd class="information-list__item__definition">(.+?)</dd>', sect3).group(1).split(",")
            except:
                primary_lang = []

            try:
                additional_lang = re.search('<p data-test-bidi>(.+?)</p>', sect3).group(1).split(",")
            except:
                additional_lang = []

            closed_captioning = False
            if "sous-titres codés (CC)" in sect3: closed_captioning = True

            subtitles_Deaf_Hard = False
            if "sourdes ou malentendantes (SDH)" in sect3: subtitles_Deaf_Hard = True

            audiodescription = False
            if "audiodescription (AD)" in sect3: audiodescription = True


            #¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
            #        Export...        #
            #_________________________#    


            yield {
                'movie_URL' : urlMo,
                
                'title': title, 'resume': resum, 'creation' : creat, 'duration' : durat,

                'categorie': categ, 'categorie_URL': caURL,
                
                'artworks_URLs' : artworks_URLs, 'pegi_info' : pegi_info, # 'badges' : badges, ----- !!!!! div non-netoyées 
                
                'rent_movie': rent_movie, 'buy_movie': buy_movie, 
                
                #'trailer_URL': trail, ------------- !!!!!!!!!!!!!!!!!!!!!!!!! imposible de recuperer attribut cree par javascript ?

                'studio' : studio, 'copyright' : copyright, 'primary_lang' : primary_lang, 'additional_lang' : additional_lang,

                'closed_captioning' : closed_captioning, 'subtitles_Deaf_Hard' : subtitles_Deaf_Hard, 'audiodescription' : audiodescription,
                
                #'squad' : squad, 'music_artists': music, ----- !!!!! div non-netoyées 

            }

print("...Import Class Function")
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
# Create Folder Directory #
#_________________________#
print("Create Folder Directory...")

try: 
    parent_dir = os.path.abspath(os.path.split(__file__)[0])
    folder_name = "src"
    print(parent_dir)

    path = os.path.join(parent_dir, folder_name)
    os.mkdir(path)
except:
    print("File probably exists")

print("...Create Folder Directory")
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#       Run Process       #
#_________________________#
print("Run Process...")

# Name of the file where the results will be saved
filename = "iTunesFilmsInfos.json"

# Settings Crawler 
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'LOG_LEVEL': logging.ERROR,
    "FEEDS": {
        path + '/' + filename : {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(QuotesSpider)
process.start()

print("...Run Process")


## 'Chrome/97.0'
## 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
## 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
## 


# https://pypi.org/project/rotating-free-proxies/ 

# https://pypi.org/project/scrapy-rotating-proxies/ # <--- detect bannissement 

# https://docs.scrapy.org/en/latest/topics/autothrottle.html#autothrottle-algorithm

# https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings

# https://github.com/scrapy-plugins/scrapy-splash#why-not-use-the-splash-http-api-directly

# https://pypi.org/project/scrapy-rotating-proxies/


# Quelques films avec le plus de données :

    # https://itunes.apple.com/fr/movie/à-demain-mon-amour/id794729993 --> Premier de la liste.
    # https://itunes.apple.com/fr/movie/ant-man-et-la-guêpe/id1405923580 --> Dolby Visio, Itunes Xtras, Accessibilité SDH & AD.
    # https://itunes.apple.com/fr/movie/black-widow-2021/id1576465482 --> Plusieurs artistes du film. 
    # https://itunes.apple.com/fr/movie/adios/id1501468448 --> Juste HD, -16, Plusieurs langues. 