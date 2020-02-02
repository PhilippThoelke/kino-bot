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

def last_sneak_movies(amount=None):
    soup = get_soup(SNEAK_URL)
    rows = soup.find_all('div', class_='wpb_column vc_column_container vc_col-sm-3')

    movies = []
    for row in rows[::2]:
        movie = row.div.div.div.div.strong.text.strip().split('\n')
        if len(movie) > 1:
            movies.append((movie[0], movie[1][11:]))
        elif len(movie) == 1:
            rating_found = False
            for child_num in range(2, 5):
                rating = row.div.div.div.div.select(f'strong:nth-child({child_num})')
                if len(rating) > 0:
                    rating_text = rating[0].text.strip()
                    if len(rating_text) > 0 and rating_text.startswith('Bewertung'):
                        movies.append((movie[0], rating_text[11:14]))
                        rating_found = True
                        break
            if not rating_found:
                movies.append((movie[0], None))
    if amount is not None and amount > 0:
        return movies[:amount]
    else:
        return movies
