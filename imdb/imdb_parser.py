import urllib
import urllib.request as urllib2

from bs4 import BeautifulSoup
import requests


class ImdbNetflixChecker:
    movie_rating = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    def fetch_top_1000_movies_from_imdb(self):
        movie_number = 1
        url_part_1 = "https://www.imdb.com/search/title?groups=top_1000&view=simple&sort=user_rating,desc&start="
        url_part_3 = "&ref_=adv_nxt"

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
                ratings = listerItem.findAll("div", {"class": "col-imdb-rating"})
                for rating in ratings:
                    rating = rating.findChildren("strong")[0].string.strip()
                    self.movie_rating[movie] = rating
            movie_number += 50

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

        with requests.Session() as session:
            url = "https://www.netflix.com/be-en/login"
            r = session.get(url, headers=self.headers)
            soup = BeautifulSoup(r.content, 'html5lib')
            login_data['authURL'] = soup.find('input', attrs={'name': 'authURL'})['value']

            r = session.post(url, data=login_data, headers=self.headers)
            return session

    def search_for_movie_on_netflix(self, movie):
        print("netflix " + movie)
        netflix_search_page = "https://www.netflix.com/search?q=" + movie.replace("'", "").replace(" ", "%20")
        print(netflix_search_page)
        html_page = urllib2.urlopen(netflix_search_page)
        contents = html_page.read()
        soup = BeautifulSoup(contents, 'lxml')
        suggestionsExist = soup.find("div")
        print(suggestionsExist)

    def perform_search_on_netflix_to_get_authurl(self, session, movie):
        netflix_search_page = "https://www.netflix.com/search?q=" + movie.replace("'", "").replace(" ", "%20")
        print("netflix search page " + netflix_search_page)
        response = session.get(netflix_search_page, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html5lib')
        scripts = soup.findAll('script')
        for script in scripts :
            if script.string is not None:
                if (script.string.find('authURL')) != -1:
                    print(script.string)
                    auth_url_begin_index = script.string.find('"authURL":"') + len('"authURL":"')
                    print(script.string[auth_url_begin_index:])

                    index_end_auth_url = script.string[auth_url_begin_index:].find('"')-1
                    print(index_end_auth_url)
                    print(script.string[auth_url_begin_index:(auth_url_begin_index - 1 + 51)])
        print(response.content)

    def fetch_json_movie_data_from_netflix(self, session, movie, authUrl):
        form_data = {
            'path': '["search","byTerm","|\"the departed\"","suggestions",20,["length","referenceId","trackIds"]]',
            'path': '["search","byTerm","|\"the departed\"","titles",48,["id","length","listId","name","referenceId","requestId","trackIds"]]',
            'path': '["search","byTerm","|\"the departed\"","suggestions",20,{"from":0,"to":20},"summary"]',
            'path': '["search","byTerm","|\"the departed\"","titles",48,{"from":0,"to":48},"summary"]',
            'path': '["search","byTerm","|\"the departed\"","titles",48,{"from":0,"to":48},"reference",["promoVideo","summary","title","titleMaturity","userRating","userRatingRequestId"]]',
            'path': '["search","byTerm","|\"the departed\"","titles",48,{"from":0,"to":48},"reference","boxarts","_342x192","webp"]',
            'authURL': '1553695239513.lqLs9m2iXIJ77lLdWxg\\x2B5KaLSVU\\x3D'
        }
        netflix_json_request = "https://www.netflix.com/api/shakti/v28c33f16/pathEvaluator?drmSystem=widevine&isWatchlistEnabled=false&isShortformEnabled=false&isVolatileBillboardsEnabled=false&falcor_server=0.1.0&withSize=true&materialize=true"
        print("netflix search page " + netflix_json_request)
        response = session.post(netflix_json_request, headers=self.headers)
        #response = session.get("https://www.netflix.com/search?q=\"the%20departed\"", headers=self.headers)
        print(response.content)

        self.get_auth_url_from_script_in_response(response.content)

        print(response)

    def get_auth_url_from_script_in_response(self, content):
        soup = BeautifulSoup(content, 'html5lib')
        scripts = soup.findAll('script')
        for script in scripts:
            print(script['value'])

    @staticmethod
    def decode_hex_signs(str):
        begin_escape_index = str.find('\\x')
        while begin_escape_index != -1:
            characters_to_replace = str[begin_escape_index:begin_escape_index+4]
            str = str.replace(characters_to_replace, bytearray.fromhex(characters_to_replace[2:]).decode("utf-8"))
            begin_escape_index = str.find('\\x')
        return str

    def anaylyse_netflix_json_response(self):
        json_response = {
"jsonGraph":{
    "search":{
        "byTerm":{
            "|\"the departed\"":{
                "suggestions":{
                    "20":{
                        "$type":"ref",
                        "value":[
                            "search",
                            "byReference",
                            "f34b1ecd68e31bcb8e93f699afa2a42453298146:65eca661fbdeb9232e06a82adc9b2b9193c5aef5"
                        ]
                    }
                },
                "titles":{
                    "48":{
                        "$type":"ref",
                        "value":[
                            "search",
                            "byReference",
                            "71f6caf869dc91b4ccfe971d5208347dae7ea294:aac1987472ad48438587a990d74918f971f3bf21"
                        ]
                    }
                }
            }
        },
        "byReference":{
            "f34b1ecd68e31bcb8e93f699afa2a42453298146:65eca661fbdeb9232e06a82adc9b2b9193c5aef5":{
                "length":{
                    "$type":"atom",
                    "value":2
                },
                "referenceId":{
                    "$type":"atom",
                    "value":"f34b1ecd68e31bcb8e93f699afa2a42453298146:65eca661fbdeb9232e06a82adc9b2b9193c5aef5"
                },
                "trackIds":{
                    "$type":"atom",
                    "$size":98,
                    "value":{
                        "trackId":13752290,
                        "trackId_jaw":13752290,
                        "trackId_jawEpisode":13752290,
                        "trackId_jawTrailer":13752290
                    }
                },
                "0":{
                    "summary":{
                        "$type":"atom",
                        "$size":112,
                        "value":{
                            "entityId":"81048910_video",
                            "type":"video",
                            "id":81048910,
                            "name":"LEGO Ninjago: Masters of Spinjitzu: Day of the Departed"
                        }
                    }
                },
                "1":{
                    "summary":{
                        "$type":"atom",
                        "$size":85,
                        "value":{
                            "entityId":"70060938_video",
                            "type":"video",
                            "id":70060938,
                            "name":"The Departed: Bonus Material"
                        }
                    }
                },
                "2":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "3":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "4":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "5":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "6":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "7":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "8":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "9":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "10":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "11":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "12":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "13":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "14":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "15":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "16":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "17":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "18":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "19":{
                    "summary":{
                        "$type":"atom"
                    }
                },
                "20":{
                    "summary":{
                        "$type":"atom"
                    }
                }
            },
            "71f6caf869dc91b4ccfe971d5208347dae7ea294:aac1987472ad48438587a990d74918f971f3bf21":{
                "length":{
                    "$type":"atom",
                    "value":2
                },
                "referenceId":{
                    "$type":"atom",
                    "value":"71f6caf869dc91b4ccfe971d5208347dae7ea294:aac1987472ad48438587a990d74918f971f3bf21"
                },
                "0":{
                    "reference":{
                        "$type":"ref",
                        "value":[
                            "videos",
                            "70044689"
                        ]
                    },
                    "summary":{
                        "$type":"atom",
                        "$size":69,
                        "value":{
                            "entityId":"70044689_video",
                            "type":"video",
                            "id":70044689,
                            "name":"The Departed"
                        }
                    }
                },
                "trackIds":{
                    "$type":"atom",
                    "$size":98,
                    "value":{
                        "trackId":13752289,
                        "trackId_jaw":13752289,
                        "trackId_jawEpisode":13752289,
                        "trackId_jawTrailer":13752289
                    }
                },
                "1":{
                    "summary":{
                        "$type":"atom",
                        "$size":73,
                        "value":{
                            "entityId":"80190149_video",
                            "type":"video",
                            "id":80190149,
                            "name":"All Hallows' Eve"
                        }
                    },
                    "reference":{
                        "$type":"ref",
                        "value":[
                            "videos",
                            "80190149"
                        ]
                    }
                },
                "2":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "3":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "4":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "5":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "6":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "7":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "8":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "9":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "10":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "11":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "12":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "13":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "14":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "15":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "16":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "17":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "18":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "19":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "20":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "21":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "22":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "23":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "24":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "25":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "26":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "27":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "28":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "29":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "30":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "31":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "32":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "33":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "34":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "35":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "36":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "37":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "38":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "39":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "40":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "41":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "42":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "43":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "44":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "45":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "46":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "47":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                },
                "48":{
                    "summary":{
                        "$type":"atom"
                    },
                    "reference":{
                        "$type":"atom"
                    }
                }
            }
        }
    },
    "videos":{
        "80190149":{
            "promoVideo":{
                "$type":"atom",
                "$size":34,
                "value":{
                    "id":80190345,
                    "start":0,
                    "computeId":""
                }
            },
            "summary":{
                "$type":"atom",
                "$size":57,
                "value":{
                    "id":80190149,
                    "type":"movie",
                    "isNSRE":"false",
                    "isOriginal":"false"
                }
            },
            "title":{
                "$type":"atom",
                "value":"All Hallows' Eve"
            },
            "titleMaturity":{
                "$type":"atom",
                "$size":10,
                "value":{
                    "level":41
                }
            },
            "userRatingRequestId":{
                "$type":"atom",
                "value":"bdc977ee-23cf-4626-80dd-70ada5cec249-158403498"
            },
            "userRating":{
                "$type":"atom",
                "$size":70,
                "value":{
                    "type":"thumb",
                    "matchScore":"",
                    "userRating":0,
                    "tooNewForMatchScore":"false"
                }
            },
            "boxarts":{
                "_342x192":{
                    "webp":{
                        "$type":"atom",
                        "$size":256,
                        "value":{
                            "url":"https://occ-0-767-1335.1.nflxso.net/dnm/api/v6/0DW6CdE4gYtYx8iy3aj8gs9WtXE/AAAABUIgqr78bRSxEciaS9qHMS9YrFWXJkH32sq5wrmumNgWhDbc2zXbkOuaLhzYy6aJ_rApt4omhtXvO-oTdt1tFbSv0EGbVQjj.webp?r=c20",
                            "image_key":"sdp,4|AD_5b689281-5874-11e7-a4ee-12f259fdd4aa|en|OJN"
                        }
                    }
                }
            }
        },
        "70044689":{
            "promoVideo":{
                "$type":"atom",
                "$size":34,
                "value":{
                    "id":81038547,
                    "start":0,
                    "computeId":""
                }
            },
            "summary":{
                "$type":"atom",
                "$size":57,
                "value":{
                    "id":70044689,
                    "type":"movie",
                    "isNSRE":"false",
                    "isOriginal":"false"
                }
            },
            "title":{
                "$type":"atom",
                "value":"The Departed"
            },
            "titleMaturity":{
                "$type":"atom",
                "$size":11,
                "value":{
                    "level":110
                }
            },
            "userRatingRequestId":{
                "$type":"atom",
                "value":"bdc977ee-23cf-4626-80dd-70ada5cec249-158403498"
            },
            "userRating":{
                "$type":"atom",
                "$size":70,
                "value":{
                    "type":"thumb",
                    "matchScore":"",
                    "userRating":0,
                    "tooNewForMatchScore":"false"
                }
            },
            "boxarts":{
                "_342x192":{
                    "webp":{
                        "$type":"atom",
                        "$size":256,
                        "value":{
                            "url":"https://occ-0-767-1335.1.nflxso.net/dnm/api/v6/0DW6CdE4gYtYx8iy3aj8gs9WtXE/AAAABUh3siGomJhNGDZfeQPGs9m2Ycx6oKqGsTvE-dRIemYR_NPGzmgseFESR8WVAqXe9iQD5xbtgb6IND7R0o80Mc4OYUqkRa4r.webp?r=aa4",
                            "image_key":"sdp,4|AD_0bb1a8c3-3d3d-11e5-8112-0f22b9b73b4a|en|OJN"
                        }
                    }
                }
            }
        }
    }
},
"paths":[
    [
        "search",
        "byTerm",
        "|\"the departed\"",
        "suggestions",
        "20",
        [
            "length",
            "referenceId",
            "trackIds"
        ]
    ],
    [
        "search",
        "byTerm",
        "|\"the departed\"",
        "titles",
        "48",
        [
            "id",
            "length",
            "listId",
            "name",
            "referenceId",
            "requestId",
            "trackIds"
        ]
    ],
    [
        "search",
        "byTerm",
        "|\"the departed\"",
        "suggestions",
        "20",
        {
            "from":0,
            "to":20
        },
        "summary"
    ],
    [
        "search",
        "byTerm",
        "|\"the departed\"",
        "titles",
        "48",
        {
            "from":0,
            "to":48
        },
        "summary"
    ],
    [
        "search",
        "byTerm",
        "|\"the departed\"",
        "titles",
        "48",
        {
            "from":0,
            "to":48
        },
        "reference",
        [
            "promoVideo",
            "summary",
            "title",
            "titleMaturity",
            "userRating",
            "userRatingRequestId"
        ]
    ],
    [
        "search",
        "byTerm",
        "|\"the departed\"",
        "titles",
        "48",
        {
            "from":0,
            "to":48
        },
        "reference",
        "boxarts",
        "_342x192",
        "webp"
    ]
]
}

        print(json_response['jsonGraph']['search']['byTerm'])


test = ImdbNetflixChecker()
test.anaylyse_netflix_json_response()
#test.decode_hex_signs("1553695239513.lqLs9m2iXIJ77lLdWxg\\x2B5KaLSVU\\x3D")
#test.fetch_top_1000_movies_from_imdb()
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
