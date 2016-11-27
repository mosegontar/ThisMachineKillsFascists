import os

import tweepy
from config import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class SongRetriever(object):

    def __init__(self):
        self.songs = [f for f in os.listdir(os.getcwd()+'/lyrics') if f.endswith('.txt')]

    def get_lyrics(self, file_name):
        lyrics = None
        with open('lyrics/'+file_name, 'r') as f:
            lyrics = [line.strip('\n') for line in f.readlines() if not (line == '\n' or line == '')]

        return lyrics

    def get_song(self, tweet_text):
        
        text = set([word.lower() for word in tweet_text.split() if len(word) > 3])

        matches = []
        for song in self.songs:
            keywords = set(map(lambda s: s.lower(), song.split('.txt')[0].split()))
            found = list(keywords.intersection(text))
            if len(found) > 0:
                matches.append((song, len(found)))

        if matches:
            found_match = sorted(matches, key=lambda x: x[1], reverse=True)[0][0]
            song_title, song_lyrics = found_match.strip('.txt'), self.get_lyrics(found_match)
            return song_title, song_lyrics

        return False        

class MyStreamListener(tweepy.StreamListener):

    song_retriever = SongRetriever()

    def on_error(self, status_code):
        if status_code == 420:
            api.update_status('Temporarily offline; permanently bound for glory.')
            return False    

    def on_status(self, status):
        
        screen_name = '@'+status.user.screen_name
        status_id = status.id_str
        
        song_to_sing, song_lyrics = MyStreamListener.song_retriever.get_song(status.text)

        if not song_to_sing:
            self.send_reply("Hey, I couldn't find a song in my catalog from the words in your tweet")
        else:
            song_length = len(song_lyrics)
            count = 1
            for line in song_lyrics:
                line_number = '{0}/{1}'.format(count, song_length)
                self.send_reply(song_to_sing, line, line_number, screen_name, status_id)
                count += 1

    def send_reply(self, song_to_sing, line, line_number, screen_name, status_id):

        message = '{0} {1} ({2} {3})'.format(screen_name,
                                             line, 
                                             song_to_sing.title(), 
                                             line_number)

        if line_number.split('/')[0] == '1':
            api.update_status(message, in_reply_to_status_id = status_id) 
        else:
            for status in tweepy.Cursor(api.user_timeline).items():
                api.update_status(message, in_reply_to_status_id=status.id)
                break


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['@singtomewoody'])
"""
for status in tweepy.Cursor(api.user_timeline).items():
    api.destroy_status(status.id)
"""
