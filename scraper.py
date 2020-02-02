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
    rows = soup.find_all('div', class_=LAST_SNEAKS_ROW_CSS_SELECTOR)

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

    if amount == 1:
        message = LAST_1_SNEAKS_MESSAGE
        movies = movies[:1]
    elif amount is None:
        message = LAST_SNEAKS_MESSAGE.format(len(movies))
    else:
        message = LAST_SNEAKS_MESSAGE.format(amount)
        movies = movies[:amount]

    for movie, rating in movies:
        if rating is None:
            rating = 'keine Bewertung'
        message += f'\n{movie} ({rating})'
    return message