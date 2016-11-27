import requests
from bs4 import BeautifulSoup



class Importer(object):

    def __init__(self, song_url, title):
        self.url =  'http://www.woodyguthrie.org/Lyrics/' + song_url
        self.title = title
        self.lyrics = []

    def get_lyrics(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        verses = soup.find_all('p', {'class': 'LyricText'})
        
        if not verses:
            print(self.title)



def get_song_titles():
    songs = []
    request = requests.get('http://www.woodyguthrie.org/Lyrics/Lyrics.htm')
    soup = BeautifulSoup(request.text, 'html.parser')
    lyric_links = soup.find_all('p', {'class': 'SongTitleLinks'})
    for link in lyric_links:
        url = link.find('a').get('href')
        title = link.get_text()
        songs.append((url, title))
    for a, t in songs:
        songImport = Importer(a, t)
        songImport.get_lyrics()
        print()



get_song_titles()
