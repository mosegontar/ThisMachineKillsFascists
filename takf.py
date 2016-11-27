import os

import tweepy
from config import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


songs = [f for f in os.listdir(os.getcwd()+'/lyrics') if f.endswith('.txt')]

class MyStreamListener(tweepy.StreamListener):

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False    

    def on_status(self, status):
        
        screen_name = '@'+status.user.screen_name
        status_id = status.in_reply_to_status_id
        
        song_to_sing = self.get_song(status.text)

        if not song_to_sing:
            pass
        else:
            self.send_reply(song_to_sing, screen_name, status_id)

    def get_song(self, tweet_text):
        
        text = set([word for word in tweet_text.split() if len(word) > 3])

        matches = []
        for song in songs:
            keywords = set(song.split('.txt')[0].split())
            found = list(keywords.intersection(text))
            if len(found) > 0:
                matches.append((song, len(found)))

        if matches:
            song_to_sing = sorted(matches, key=lambda x: x[1], reverse=True)[0]
            return song_to_sing

        return False

    def send_reply(self, song, screen_name, status_id):
        api.update_status('{0} {1}'.format(screen_name, song), status_id)        



#myStreamListener = MyStreamListener()
#myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

#myStream.filter(track=['@singtomewoody'])

