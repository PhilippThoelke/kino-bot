import requests
from bs4 import BeautifulSoup
import logging
from constants import *

logger = logging.getLogger(__name__)

def get_soup(url):
    response = requests.get(url)
    if response.ok:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        logger.warning(f'Couldn\'t get a response from "{url}"')

def sneak_info():
    soup = get_soup(SNEAK_URL)
    if soup is None:
        return None
    return SNEAK_INFO_MESSAGE.format(soup.select(NEXT_SNEAK_CSS_SELECTOR)[0].text)
