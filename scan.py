import fnmatch
import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC
from pykakasi import kakasi, wakati

from icelrc.scrapers import pprint
from icelrc.search import search
from icelrc.models import Lyric

kakasi = kakasi()
kakasi.setMode('H','a') # default: Hiragana no conversion
kakasi.setMode('K','a') # default: Katakana no conversion
kakasi.setMode('J','a') # default: Japanese no conversion
kakasi.setMode('r','Hepburn') # default: use Hepburn Roman table
kakasi.setMode('C', False) # add space default: no Separator
kakasi.setMode('c', False) # capitalize default: no Capitalize
kakasi = kakasi.getConverter()

wakati = wakati()
wakati = wakati.getConverter()

def scan():
    file_paths = []
    for root, dirnames, filenames in os.walk('/mnt/d/Music'):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            file_paths.append(os.path.join(root, filename))

    for file_path in file_paths:
        mp3info = dict(EasyID3(file_path).items())
        title = mp3info.get('title', [0])[0]
        artist = mp3info.get('artist', [0])[0]
        if title and artist:
            tags = ID3(file_path)
            print(title, '     ', artist)
            lyrics = USLT()
            print("LYRICS:", lyrics)
            try:
                lyrics = Lyric.objects.get(title=title, artist=artist).lyrics
                print("Lyrics Exist")
            except Lyric.DoesNotExist:
                pass
                # romanized_title = kakasi.do(wakati.do(title))
                # romanized_artist = kakasi.do(artist)

                # lyrics = (
                #     search(romanized_title + ' ' + romanized_artist) or
                #     search(romanized_title + ' ' + artist) or
                #     search(title + ' ' + artist) or
                #     search(title) or
                #     search(romanized_title) or
                #     ""
                # )

                # if lyrics:
                #     Lyric.objects.create(title=title, artist=artist, lyrics=lyrics)
                #     print("Found Lyrics")
            
            # input('Press Enter to Continue...')

            # print(lyrics)
            print('='*20)

def apply():
    file_paths = []
    for root, dirnames, filenames in os.walk('/mnt/d/Music'):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            file_paths.append(os.path.join(root, filename))

    for file_path in file_paths:
        mp3info = dict(EasyID3(file_path).items())
        title = mp3info.get('title', [0])[0]
        artist = mp3info.get('artist', [0])[0]
        if title and artist:
            tags = ID3(file_path)
            try:
                lyrics = Lyric.objects.get(title=title, artist=artist).lyrics
                print("Lyrics Exist")
                uslt = USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics)
                print(uslt)
                tags[u"USLT::'eng'"] = uslt
                tags.save(file_path)
            except Lyric.DoesNotExist:
                pass