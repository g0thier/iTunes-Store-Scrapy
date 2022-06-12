# iTunes-Store-Scrapy
- Scrapy Films of iTunes Store France

## Script01 :

- Scrap Genres : https://itunes.apple.com/fr/genre/films/id33 
- to list : iTunesCategories.json

## Script02 :

- Adding [AZ] to : iTunesCategories.json
- for export : url_list.txt

## Script03 :

- Scrap url_list.txt ( exemple : https://itunes.apple.com/fr/genre/films-action-et-aventure/id4401?letter=A )
- to obtain numbers of pages : iTunesPages.json

## Script04 :

- Scrap iTunesPages.json ( exemple : https://itunes.apple.com/fr/genre/films-action-et-aventure/id4401?letter=F&page=1#page )
- to obtain : iTunesFilmsCollection.json

## Script05 : 

- Scrap iTunesFilmsCollection.json ( exemple : https://itunes.apple.com/fr/movie/ant-man-et-la-guêpe/id1405923580 )
- for obtain dataset : iTunesFilmsInfos.json

# Ask for corrections Script05 :
* -> duplicate results ???
* -> can get "trailer_URL" cause to javascript generate URL for this one.
* -> I don't have time for get keyworks of "badges" ( you can use same process than CC, SDH and AD with sect3 )  
* -> I don't have time for get squad and music_artists 

the rest works
