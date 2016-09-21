import requests, re
from bs4 import BeautifulSoup
from icelrc.utils import pprint, LyricNotFound

class BaseScraper(object):
    base_url = ''

    def get_lyrics(self, url):
        raise NotImplementedError('Not Implemented')

    def clean_lyrics(self, lyrics):
        if not lyrics:
            raise LyricNotFound('Lyrics Not Found')
                
        lyrics = lyrics.strip()
        lyrics = re.sub('\n{3,}','\n\n', lyrics)

        return lyrics


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

        return self.clean_lyrics(lyrics)

class AnimeLyricsScraper(BaseScraper):
    base_url = 'www.animelyrics.com'

    def get_lyrics(self, url, lang='romaji'):
        # <br> tags behave strangely on animelyrics.com for some reason
        soup = BeautifulSoup( requests.get(url).text.replace('<br>', '&#10;'), 'html.parser')

        for dt in soup.find_all('dt'): 
            dt.decompose()

        find_id = {
            'romaji'  : 'romaji',
            'english' : 'translation',
        }.get(lang)

        lyrics = '\n'.join([
            lrc.get_text() 
            for lrc in soup.find_all('span', {'class': 'lyrics'}) 
            if find_id in lrc.parent.attrs.get('class', None)
        ])

        return self.clean_lyrics(lyrics)

class VocaLyricsScraper(BaseScraper):
    base_url = 'voca-lyrics.blogspot.com'

    def get_lyrics(self, url, lang='romaji'):
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        lyrics = soup.find('div',{'class': 'post-body'}).get_text()

        return self.clean_lyrics(lyrics)

class VocaloidLyricsScraper(BaseScraper):
    base_url = 'vocaloidlyrics.wikia.com'

    def get_lyrics(self, url, lang='romaji'):
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        lyrics = soup.find('table', {'style' : 'width:100%'}).get_text()

        return self.clean_lyrics(lyrics)


class JPopAsiaScraper(BaseScraper):
    base_url = 'www.jpopasia.com'

    def get_lyrics(self, url, lang='romaji'):
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        if soup.find(id='tabLyrics'):
            # new layout
            find_id = {
                'romaji' : 'romaji_1'
            }.get(lang)

            lyrics = soup.find(id=find_id).get_text()
        else:
            # old layout
            for div in soup.find_all('div',{'class': 'col-sm-4'}):
                if lang.title() in div.get_text():
                    lyrics = div.get_text()
                    break

        return self.clean_lyrics(lyrics)