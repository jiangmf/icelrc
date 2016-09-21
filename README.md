# icelrc

A personal lyrics management tool for my music library.
Note that this is just a quick and dirty tool for my own needs, I paid no attention to code quality or ease of use.

### How it works:
1. Scans my music library (specified in settings.py) for any .mp3 files
2. Fetches the title and artist from ID3 tags in the .mp3 file using mutagen.
3. Checks the database for any matching lyrics with the same title and artist name.
4. If there are no matching lyrics, it searches google for the lyrics, converting the title from japanese to romaji using pykakasi if nessisary.
5. Using a list of defined scrapers for various site, fetch the lyrics from page source and store it in the data base.
6. Set the UNSYNCEDLYRICS tag for my .mp3 files using mutagen.

Also features an admin page that allows me to bulk edit lyrics to fix/clean up any thing that doesn't look right.
