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
file_name = "iTunesCategories.json"

path = os.path.join(parent_dir, folder_name, file_name)

# ouverture du fichier
file = open(path)
results = json.load(file)

## Tableau sous numpy 
df = pd.DataFrame(results)

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#     Create list A-Z     #
#_________________________#

azertyList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '#']
url_list = []

for index in range(len(df)):
    
    item = df["URL"][index]

    for abc in azertyList: 
        url_list.append(item+'?letter='+abc)

print(url_list)

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#      Record as txt      #
#_________________________#

file_name = "url_list.txt"
path = os.path.join(parent_dir, folder_name, file_name)

textfile = open(path, "w")
for element in url_list:
    textfile.write(element + "\n")
textfile.close()