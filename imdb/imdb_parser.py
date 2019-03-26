from html.parser import HTMLParser
import urllib.request as urllib2
from bs4 import BeautifulSoup
import requests

class ImdbScraper:

    movie_rating = {}

    def tryWithBs(self):
        html_page = urllib2.urlopen("https://www.imdb.com/search/title?groups=top_250&view=simple&sort=user_rating,desc&ref_=adv_prv")
        contents = html_page.read()
        soup = BeautifulSoup(contents, 'lxml')

        listerItems = soup.findAll("div", {"class": "lister-item mode-simple"})
        for listerItem in listerItems:
            coltitle = listerItem.findAll("div", {"class": "col-title"})
            movie = ''
            for col in coltitle:
                children = col.findChildren("a")
                for child in children:
                    movie = child.string
                    print(child.string)
            ratings = listerItem.findAll("div", {"class": "col-imdb-rating"})
            for rating in ratings:
                print(rating.findChildren("strong")[0].string.strip())
                rating = rating.findChildren("strong")[0].string.strip()
                self.movie_rating[movie] =  rating

    def findMovieOnNetflix(self, movie):
        print("netflix " + movie)
        netflixSearchPage = "https://www.netflix.com/search?q=" + movie.replace("'", "").replace(" ", "%20")
        print(netflixSearchPage)
        html_page = urllib2.urlopen(netflixSearchPage)
        contents = html_page.read()
        soup = BeautifulSoup(contents, 'lxml')

#        suggestionsExist = soup.find("div", {"class": "suggestions"})
        suggestionsExist = soup.find("div")
        print(suggestionsExist)

    def testLogin(self, movie):
        url = movie
        values = {'userLoginId': 'woutmilants@gmail.com',
          'password': 'netflixWouter2019'}

        r = requests.post(url, data=values)
        print(r.content)



test = ImdbScraper()
test.tryWithBs()


#test.findMovieOnNetflix("schindlers list")
test.testLogin("https://www.netflix.com/be-en/Login?nextpage=https%3A%2F%2Fwww.netflix.com%2Fsearch%3Fq%3Dschindlers%2Blist")

#print(test.movie_rating)
#for key in test.movie_rating:
#    test.findMovieOnNetflix(key)




