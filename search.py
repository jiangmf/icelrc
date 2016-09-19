from google import search as google_search
from icelrc.settings import SCRAPERS

def search(search_term):
    urls = list(google_search(search_term + " lyrics", stop=10))
    for scraper in SCRAPERS:
        for url in urls:
            if scraper.base_url in url:
                try:
                    print("TRYING: ", scraper.__class__.__name__)
                    return scraper.get_lyrics(url)
                except:
                    import traceback; traceback.print_exc();