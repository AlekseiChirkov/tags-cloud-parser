import bs4
import requests

URL = 'https://habr.com'
RES = requests.get(URL)
SOUP = bs4.BeautifulSoup(RES.content, 'html.parser')
DATA_PATH = '/home/scareface/Documents/Projects/articles-parser/src/data'
