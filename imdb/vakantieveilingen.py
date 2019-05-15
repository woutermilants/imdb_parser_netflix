import urllib.request as urllib2
import json
import os
import ssl

from bs4 import BeautifulSoup
import requests


class vakantie_veilingen:
    movie_rating = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    def login(self):
        login_data = {
            'login': 'woutmilants@hotmail.com',
            'password': 'wouter159357'
        }

        session = requests.Session()
        url = "https://www.vakantieveilingen.be/login.html"
        request = requests.Request('GET', url, headers=self.headers)
        prepared_request = session.prepare_request(request)
        response = session.send(prepared_request)

        soup = BeautifulSoup(response.content, 'html5lib')
        login_data['authURL'] = soup.find('input', attrs={'name': 'authURL'})['value']

        session.post(url, data=login_data, headers=self.headers)
        return session




test = movi()
#test.get_imdb_top_movies_that_are_on_netflix()
test.get_imdb_top_documentaries_that_are_on_netflix()
