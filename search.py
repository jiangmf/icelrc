from google import search as google_search
from icelrc.settings import SCRAPERS
from icelrc.utils import LyricNotFound

def search(search_term):
    print("Searching for '{} lyrics' ...".format(search_term))
    urls = list(google_search(search_term + " lyrics", stop=10, pause=0.5))
    for scraper in SCRAPERS:
        for url in urls:
            if scraper.base_url in url:
                try:
                    print("TRYING: ", scraper.__class__.__name__)
                    return scraper.get_lyrics(url)
                except LyricNotFound:
                    pass
                except:
                    import traceback; traceback.print_exc();