import takf

def test_tweepy_import():
    print(takf.tweepy)

def test_import_config_keys():
    assert 'consumer_key' in takf.keys

def test_auth():
    twts = takf.api.search(q="Woody Guthrie")
    assert len(twts) > 0

def test_partial_matching():
    bot = takf.MyStreamListener()
    song_title, song_lyrics = bot.song_retriever.get_song('stetson')
    assert 'stetson' in song_title
