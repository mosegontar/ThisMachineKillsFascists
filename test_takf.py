import takf

def test_tweepy_import():
    print(takf.tweepy)

def test_import_config_keys():
    assert takf.keys['consumer_key'] == 'npDclx6ns0cIeQvs2bea7VigG'

def test_auth():
    twts = takf.api.search(q="Woody Guthrie")
    assert len(twts) > 0

def test_partial_matching():
    bot = takf.MyStreamListener()
    song = bot.get_song('trump')[0]
    assert 'trump' in song
