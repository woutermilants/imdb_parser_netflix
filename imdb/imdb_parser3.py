import urllib.request as urllib2
import json
import os
import ssl

from bs4 import BeautifulSoup
import requests


class ImdbNetflixChecker:
    movie_rating = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    def fetch_top_1000_movies_from_imdb(self):

        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        movie_number = 1
        url_part_1 = "http://www.imdb.com/search/title?groups=top_1000&view=simple&sort=user_rating,desc&start="
        url_part_3 = "&ref_=adv_nxt"

        while movie_number < 1000:
            imdb_url = url_part_1 + str(movie_number) + url_part_3
            print(imdb_url)
            html_page = urllib2.urlopen(imdb_url)
            contents = html_page.read()
            soup = BeautifulSoup(contents, 'lxml')

            listerItems = soup.findAll("div", {"class": "lister-item mode-simple"})
            for listerItem in listerItems:
                coltitle = listerItem.findAll("div", {"class": "col-title"})
                movie = ''
                for col in coltitle:
                    children = col.findChildren("a")
                    for child in children:
                        print(child.string)
                        movie = child.string
                ratings = listerItem.findAll("div", {"class": "col-imdb-rating"})
                for rating in ratings:
                    rating = rating.findChildren("strong")[0].string.strip()
                    self.movie_rating[movie] = rating
            movie_number += 50
            print("number of movies processed : " + str(movie_number))

    def is_movie_on_netflix_according_to_flickmetrix(self, movie):
        # headers = {
        # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        # 'Authorization': 'Bearer 41JkBXatKKD04Z18pV3npQ=='
        # }

        headers = {
            'Host': 'flickmetrix.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Response': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Referer': 'https://flickmetrix.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,nl-NL;q=0.8,nl;q=0.7',
            'Cookie': '_ga=GA1.2.1076896268.1553805034; _gid=GA1.2.322205118.1553805034',
        }
        session = requests.Session()

        # url = "https://flickmetrix.com/api/values/getFilms?amazonRegion=us&cast=&comboScoreMax=100&comboScoreMin=0&countryCode=be&currentPage=0&deviceID=1&director=&genreAND=false&imdbRatingMax=10&imdbRatingMin=0&imdbVotesMax=1600000&imdbVotesMin=0&inCinemas=true&includeDismissed=true&includeSeen=true&includeWantToWatch=true&isCastSearch=false&isDirectorSearch=false&language=all&letterboxdScoreMax=100&letterboxdScoreMin=0&letterboxdVotesMax=1400000&letterboxdVotesMin=0&metacriticMax=100&metacriticMin=0&netflixRegion=be&onAmazonPrime=false&onAmazonVideo=false&onDVD=false&onNetflix=false&pageSize=20&plot=&popularityMax=100&popularityMin=0&queryType=GetFilmsToSieve&rtCriticFreshMax=300&rtCriticFreshMin=0&rtCriticMeterMax=100&rtCriticMeterMin=0&rtCriticRatingMax=10&rtCriticRatingMin=0&rtCriticReviewsMax=400&rtCriticReviewsMin=0&rtCriticRottenMax=200&rtCriticRottenMin=0&rtUserMeterMax=100&rtUserMeterMin=0&rtUserRatingMax=5&rtUserRatingMin=0&rtUserReviewsMax=40000000&rtUserReviewsMin=0&searchTerm=the+departed&sortOrder=comboScoreDesc&title=&token=41JkBXatKKD04Z18pV3npQ%3D%3D&watchedRating=0&writer=&yearMax=2019&yearMin=1900"
        url = "https://flickmetrix.com/api/values/getFilms?amazonRegion=us&cast=&comboScoreMax=100&comboScoreMin=0&countryCode=be&currentPage=0&deviceID=1&director=&genreAND=false&imdbRatingMax=10&imdbRatingMin=0&imdbVotesMax=1600000&imdbVotesMin=0&inCinemas=true&includeDismissed=true&includeSeen=true&includeWantToWatch=true&isCastSearch=false&isDirectorSearch=false&language=all&letterboxdScoreMax=100&letterboxdScoreMin=0&letterboxdVotesMax=1400000&letterboxdVotesMin=0&metacriticMax=100&metacriticMin=0&netflixRegion=be&onAmazonPrime=false&onAmazonVideo=false&onDVD=false&onNetflix=false&pageSize=20&plot=&popularityMax=100&popularityMin=0&queryType=GetFilmsToSieve&rtCriticFreshMax=300&rtCriticFreshMin=0&rtCriticMeterMax=100&rtCriticMeterMin=0&rtCriticRatingMax=10&rtCriticRatingMin=0&rtCriticReviewsMax=400&rtCriticReviewsMin=0&rtCriticRottenMax=200&rtCriticRottenMin=0&rtUserMeterMax=100&rtUserMeterMin=0&rtUserRatingMax=5&rtUserRatingMin=0&rtUserReviewsMax=40000000&rtUserReviewsMin=0&searchTerm=" + movie.replace(
            ' ', '+') + "&sortOrder=comboScoreDesc&title=&token=&watchedRating=0&writer=&yearMax=2019&yearMin=1900"
        #url = "https://facebook.com"
        #r = session.get(url, headers=headers)
        request = requests.Request('GET', url, headers=headers)
        prepared_request = session.prepare_request(request)
        response = session.send(prepared_request)
        json_string = response.json()
        valid_json = json.loads(json_string)[0]

        #print("is " + movie + " on netflix ? " + str(valid_json['onNetflix']))
        return valid_json

    def login_to_netflix(self):
        login_data = {
            'userLoginId': 'woutmilants@gmail.com',
            'password': 'netflixWouter2019',
            'rememberMe': 'true',
            'flow': 'websiteSignUp',
            'mode': 'login',
            'action': 'loginAction',
            'withFields': 'rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode',
            'nextPage': '',
            'showPassword': '',
            'countryCode': '+32',
            'countryIsoCode': 'BE'}

        session = requests.Session()
        url = "https://www.netflix.com/be-nl/login"
        request = requests.Request('GET', url, headers=self.headers)
        prepared_request = session.prepare_request(request)
        response = session.send(prepared_request)

        soup = BeautifulSoup(response.content, 'html5lib')
        login_data['authURL'] = soup.find('input', attrs={'name': 'authURL'})['value']

        #login_request = requests.Request('POST', url, data=login_data, headers=self.headers)
        #login_prepared_request = session.prepare_request(login_request)
        #session.send(login_prepared_request)
        #return session
        r = session.post(url, data=login_data, headers=self.headers)
        return session

    def is_it_really_on_netflix(self, session, netflix_movie_id):
        url = "https://www.netflix.com/watch/" + str(netflix_movie_id)

        request = requests.Request('GET', url, headers=self.headers)
        prepared_request = session.prepare_request(request)
        response = session.send(prepared_request, allow_redirects=False)
        #print(response.status_code)
        #print(movie)
        return response.status_code == 200


test = ImdbNetflixChecker()
test.fetch_top_1000_movies_from_imdb()
print("Following movies are on netflix")
#test.movie_rating["Interstellar"] = "9"
session = test.login_to_netflix()
for movie in test.movie_rating:
    try:
        flick_metrix_response = test.is_movie_on_netflix_according_to_flickmetrix(movie)
        if flick_metrix_response['onNetflix']:
            if test.is_it_really_on_netflix(session, flick_metrix_response['netflixID']):
                print(movie + ". Imdb rating : " + test.movie_rating[movie])
    except:
        pass

