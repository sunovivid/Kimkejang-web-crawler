from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import HTTPError
from urllib.request import URLError
from urllib.request import urlretrieve
from os import linesep
import re
import random
import datetime
from PIL import Image
import pytesseract

def getBs(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    except URLError as e:
        print('The server could not found')
    try:
        bs = BeautifulSoup(html, 'lxml')
    except AttributeError as e:
        return None
    return bs

count = 0

def getPageContent(url,title):
    image = getBs(url).body.find('div',{'class':'article'}).find('img').attrs['src']
    global count
    imageName = 'comic{0}.png'.format(count)
    urlretrieve(image,imageName)
    count += 1
    text = pytesseract.image_to_string(Image.open(imageName),lang = 'kor')
    text = text.replace('[ |\n]', "")
    print(text)
    print('                       ---COMMENT---')
    for text in getBs(url).body.find('div',{'class':'article'}).findAll('p'):
        t =  text.get_text()
        if t != ' ' and title not in t:
            print(t)
        #if '<p></p>' not in text and '<p> </p>' not in text:
        #   print(text)
    print('')
    #print(getBs(url).body.find('div',{'class':'titleWrap'}).h2.a.attrs['href'])

#PROGRAM START FROM HERE
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

startPage = 24
for pageIndex in range(1,startPage):
    bs = getBs('https://kimkero.tistory.com/category/%EB%A7%8C%ED%99%94?page={0}'.format(pageIndex))
    for child in bs.body.find('div',{'class':'searchList'}).ol:
        try:
            title = child.find('a').get_text()
            print('-----------------------------TITLE------------------------------')
            print(title)
            print('                         ---CONTENT---')
            for i in range(1,4):
                print('')
            getPageContent('https://kimkero.tistory.com/'+child.find('a').attrs['href'],title)
        except AttributeError as e:
            pass


#getPageContent('https://kimkero.tistory.com/'+child.a.attrs['href'])