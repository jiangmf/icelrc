import requests
from bs4 import BeautifulSoup

class LyricsNotFound(Exception):
    pass

def pprint(data):
    import pprint as python_pprint
    pp = python_pprint.PrettyPrinter(indent=4)
    pp.pprint(data)
    return pp.pformat(data)

class BaseScraper(object):
    base_url = ''

    def get_lyrics(self, url):
        raise NotImplementedError('Not Implemented')

class LyricalNonsenseScraper(BaseScraper):
    base_url = 'www.lyrical-nonsense.com'

    def get_lyrics(self, url, lang='romaji'):
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        for div in soup.find_all('div', {'class':'creditlyricblock2'}): 
            div.decompose()

        find_id = {
            'romaji' : 'Romaji'
        }.get(lang)

        lyrics = soup.find(id=find_id).get_text()

        if lyrics:
            return lyrics
        else:
            raise LyricsNotFound('Lyrics Not Found')

class AnimeLyricsScraper(BaseScraper):
    base_url = 'www.animelyrics.com'

    def get_lyrics(self, url, lang='romaji'):
        soup = BeautifulSoup(
            # <br> tags behave strangely on animelyrics.com for some reason
            requests.get(url).text.replace('<br>', '&#10;'), 
            'html.parser'
            )

        for dt in soup.find_all('dt'): 
            dt.decompose()

        find_id = {
            'romaji'  : 'romaji',
            'english' : 'translation',
        }.get(lang)

        lyrics = '\n'.join([
            lrc.get_text() 
            for lrc in soup.find_all('span', {'class': 'lyrics'}) 
            if find_id in lrc.parent.attrs['class']
        ])

        if lyrics:
            return lyrics
        else:
            raise LyricsNotFound('Lyrics Not Found')

class VocaLyricsScraper(BaseScraper):
    base_url = 'voca-lyrics.blogspot.com'

    def get_lyrics(self, url, lang='romaji'):
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        lyrics = soup.find('div',{'class': 'post-body'}).get_text()

        if lyrics:
            return lyrics
        else:
            raise LyricsNotFound('Lyrics Not Found')

class JPopAsiaScraper(BaseScraper):
    base_url = 'www.jpopasia.com'

    def get_lyrics(self, url, lang='romaji'):
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        # new layout
        if soup.find(id='tabLyrics'):
            find_id = {
                'romaji' : 'romaji_1'
            }.get(lang)

            lyrics = soup.find(id=find_id).get_text()
        else:
            for div in soup.find_all('div',{'class': 'col-sm-4'}):
                if lang.title() in div.get_text():
                    lyrics = div.get_text()
                    break


        if lyrics:
            return lyrics
        else:
            raise LyricsNotFound('Lyrics Not Found')