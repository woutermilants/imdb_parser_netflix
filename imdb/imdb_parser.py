import urllib
import urllib.request as urllib2

from bs4 import BeautifulSoup
import requests


class ImdbScraper:
    movie_rating = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    def parseImdbData(self):
        movie_number = 1
        url_part_1 = "https://www.imdb.com/search/title?groups=top_1000&view=simple&sort=user_rating,desc&start="
        url_part_2 = str(movie_number)
        url_part_3 = "&ref_=adv_nxt"

        #print(url_part_1 + url_part_2 + url_part_3)

        while movie_number < 1000:
            html_page = urllib2.urlopen(url_part_1 + str(movie_number) + url_part_3)
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
                        #print(child.string)
                ratings = listerItem.findAll("div", {"class": "col-imdb-rating"})
                for rating in ratings:
                    #print(rating.findChildren("strong")[0].string.strip())
                    rating = rating.findChildren("strong")[0].string.strip()
                    self.movie_rating[movie] = rating
            movie_number += 50

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

    def loginToNetflix(self):

        login_data = {
            'userLoginId': 'woutmilants@gmail.com',
            'password': 'netflixWouter2019',
            'rememberMe': 'true',
            'flow': 'websiteSignUp',
            'mode': 'login',
            'action': 'loginAction',
            'withFields': 'rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode',
            # 'authURL': 1553686009279.mJSqP1i1C/LiDe10JnHUxkXKFdw=,
            'nextPage': '',
            'showPassword': '',
            'countryCode': '+32',
            'countryIsoCode': 'BE'}

        with requests.Session() as s:
            url = "https://www.netflix.com/be-en/login"
            r = s.get(url, headers=self.headers)
            soup = BeautifulSoup(r.content, 'html5lib')
            login_data['authURL'] = soup.find('input', attrs={'name': 'authURL'})['value']

            r = s.post(url, data=login_data, headers=self.headers)
            #print(r.content)
            return s

    def fetchMovieDataFromNetflix(self, session, movie):
        netflixSearchPage = "https://www.netflix.com/search?q=" + movie.replace("'", "").replace(" ", "%20")
        print("netflix search page " + netflixSearchPage)
        response = session.get(netflixSearchPage, headers=self.headers)
        #response = session.get("https://www.netflix.com/search?q=\"the%20departed\"", headers=self.headers)
        soup = BeautifulSoup(response.content, 'html5lib')
        scripts = soup.findAll('script')
        for script in scripts :
            if (script.string != None):
                if (script.string.find('authURL')) != -1:
                    print(script.string)
                    auth_url_begin_index = script.string.find('"authURL":"') + len('"authURL":"')
                    print(script.string[auth_url_begin_index:])

                    index_end_auth_url = script.string[auth_url_begin_index:].find('"')-1
                    print(index_end_auth_url)
                    print(script.string[auth_url_begin_index:(auth_url_begin_index - 1 + 51)])
        print(response.content)

    def fetchJsonMovieDataFromNetflix(self, session, movie, authUrl):
        form_data = {
            'path': '["search","byTerm","|\"the departed\"","suggestions",20,["length","referenceId","trackIds"]]',
            'path': '["search","byTerm","|\"the departed\"","titles",48,["id","length","listId","name","referenceId","requestId","trackIds"]]',
            'path': '["search","byTerm","|\"the departed\"","suggestions",20,{"from":0,"to":20},"summary"]',
            'path': '["search","byTerm","|\"the departed\"","titles",48,{"from":0,"to":48},"summary"]',
            'path': '["search","byTerm","|\"the departed\"","titles",48,{"from":0,"to":48},"reference",["promoVideo","summary","title","titleMaturity","userRating","userRatingRequestId"]]',
            'path': '["search","byTerm","|\"the departed\"","titles",48,{"from":0,"to":48},"reference","boxarts","_342x192","webp"]',
            'authURL': '1553695239513.lqLs9m2iXIJ77lLdWxg\\x2B5KaLSVU\\x3D'
        }
        netflixJsonRequest = "https://www.netflix.com/api/shakti/v28c33f16/pathEvaluator?drmSystem=widevine&isWatchlistEnabled=false&isShortformEnabled=false&isVolatileBillboardsEnabled=false&falcor_server=0.1.0&withSize=true&materialize=true"
        print("netflix search page " + netflixJsonRequest)
        response = session.post(netflixJsonRequest, headers=self.headers)
        #response = session.get("https://www.netflix.com/search?q=\"the%20departed\"", headers=self.headers)
        print(response.content)

        self.getAuthUrlFromScriptInResponse(response.content)

        print(response)

    def getAuthUrlFromScriptInResponse(self, content):
        soup = BeautifulSoup(content, 'html5lib')
        scripts = soup.findAll('script')
        for script in scripts:
            print(script['value'])

    def decodeHexSigns(self, str):
        begin_escape_index = str.find('\\x')
        while begin_escape_index != -1:
            characters_to_replace = str[begin_escape_index:begin_escape_index+4]
            str = str.replace(characters_to_replace, bytearray.fromhex(characters_to_replace[2:]).decode("utf-8"))
            begin_escape_index = str.find('\\x')
        print(str)
        return str
        #print(bytearray.fromhex("3D2B").decode())

test = ImdbScraper()
test.decodeHexSigns("1553695239513.lqLs9m2iXIJ77lLdWxg\\x2B5KaLSVU\\x3D")
test.parseImdbData()
print("movies ")
print(test.movie_rating)

# test.findMovieOnNetflix("schindlers list")
#test.testLogin(    "https://www.netflix.com/be-en/Login?nextpage=https%3A%2F%2Fwww.netflix.com%2Fsearch%3Fq%3Dschindlers%2Blist")
#s = test.loginToNetflix()
#authUrl = test.fetchMovieDataFromNetflix(s, "the departed")
#test.fetchJsonMovieDataFromNetflix(s, "the departed", authUrl)

# print(test.movie_rating)
# for key in test.movie_rating:
#    test.findMovieOnNetflix(key)
