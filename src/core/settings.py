import bs4
import requests

URL = 'https://habr.com/ru/all/'
RES = requests.get(URL)
SOUP = bs4.BeautifulSoup(RES.content, 'html.parser')
DATA_PATH = '/home/scareface/Desktop/projects/ITMO/articles_parser/src/data'
