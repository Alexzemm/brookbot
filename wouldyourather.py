import urllib.request as urllib2
from bs4 import BeautifulSoup as Soup
import time

def wyr():
    url = "https://wouldurather.io/"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    req = urllib2.Request(url, headers=headers)
    
    page = urllib2.urlopen(req)

    soup = Soup(page, 'html.parser')

    a = soup.find(class_="question option1").get_text()
    b = soup.find(class_="question option2").get_text()

    return a, b
