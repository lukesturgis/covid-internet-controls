import codecs
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Data  :", data)


f=codecs.open("countries/test.html", 'r')
parser = MyHTMLParser()
parser.feed(f.read())


