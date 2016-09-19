import fnmatch
import os
from mutagen.easyid3 import EasyID3

from pykakasi import kakasi, wakati

from icelrc.scrapers import pprint
from icelrc.search import search
from icelrc.models import Lyric

kakasi = kakasi()
kakasi.setMode("H","a") # default: Hiragana no conversion
kakasi.setMode("K","a") # default: Katakana no conversion
kakasi.setMode("J","a") # default: Japanese no conversion
kakasi.setMode("r","Hepburn") # default: use Hepburn Roman table
kakasi.setMode("C", False) # add space default: no Separator
kakasi.setMode("c", False) # capitalize default: no Capitalize
kakasi = kakasi.getConverter()

wakati = wakati()
wakati = wakati.getConverter()

def scan():
    for root, dirnames, filenames in os.walk('/home/david/Music'):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            file_path = os.path.join(root, filename)
            try:
                mp3info = dict(EasyID3(file_path).items())
                title = mp3info['title'][0]
                artist = mp3info['artist'][0]
                print(title, "     ", artist)
                
                try:
                    lyrics = Lyric.objects.get(title=title, artist=artist).lyrics
                except Lyric.DoesNotExist:
                    romanized_title = kakasi.do(wakati.do(title))
                    
                    lyrics = search(title)
                    if not lyrics:
                        lyrics = search(romanized_title)
                    if not lyrics:
                        lyrics = search(romanized_title + " " + artist)

                    if lyrics:
                        Lyric.objects.create(title=title, artist=artist, lyrics=lyrics)
                    
                print(lyrics)
                print("="*20)
            except:
                import traceback; traceback.print_exc();