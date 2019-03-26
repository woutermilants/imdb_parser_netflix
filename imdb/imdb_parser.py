from html.parser import HTMLParser
import urllib.request as urllib2
from bs4 import BeautifulSoup

class ImdbHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []
    def handle_starttag(self, tag, attributes):
        #print("in start")
        if tag != 'div':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attributes:
            if name == 'class' and value == 'lister-item mode-simple':
                break
        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        #print("in end")
        if tag == 'div' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording :
            if '\\n' in data.strip() or not data.strip():
                return
            print("abc" + data.strip()+"cde")
            self.data.append(data)

    def print(self):
        print(*self.data)

html_page = html_page = urllib2.urlopen("https://www.imdb.com/search/title?groups=top_250&view=simple&sort=user_rating,desc&ref_=adv_prv")

#Feeding the content

parser = ImdbHtmlParser()
#parser.feed(str(html_page.read()))
#parser.print()


class Bs:

    def tryWithBs(self):
        html_page = html_page = urllib2.urlopen("https://www.imdb.com/search/title?groups=top_250&view=simple&sort=user_rating,desc&ref_=adv_prv")

        contents = html_page.read()

        soup = BeautifulSoup(contents, 'lxml')

  #      print(soup.select("div"))

        coltitle = soup.findAll("div", {"class": "col-title"})
        for col in coltitle:
            children = col.findChildren("a")
            for child in children:
                print(child.string)



test = Bs()
test.tryWithBs()




