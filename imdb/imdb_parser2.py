from html.parser import HTMLParser
import urllib.request as urllib2

class ImdbHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.movie_rating = {}
    def handle_starttag(self, tag, attributes):
      #  print("in start")
        if tag != 'div':
            return
        for name, value in attributes:
            if name == 'class' and value == 'lister-item mode-simple':
                self.extract_movie_and_rating(tag, attributes)
                break

 #   def handle_endtag(self, tag):
 #       print("in end")
 #     if tag == 'div':
 #           self.recording -= 1

 #   def handle_data(self, data):
 #       if self.recording :
 #           if '\\n' in data.strip() or not data.strip():
 #               return
 #           print("abc" + data.strip()+"cde")
 #           self.data.append(data)

    def extract_movie_and_rating(self, tag, attributes):
        print (tag)
        print(attributes)

    def print(self):
        print(*self.data)

html_page = html_page = urllib2.urlopen("https://www.imdb.com/search/title?groups=top_250&view=simple&sort=user_rating,desc&ref_=adv_prv")

#Feeding the content

parser = ImdbHtmlParser()
parser.feed(str(html_page.read()))
parser.print()


