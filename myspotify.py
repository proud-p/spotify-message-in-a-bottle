import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import configparser
import pandas as pd

# Spotify Auth Function
class SpotifyAuth:
    def __init__(self,keys_path):
        config = configparser.ConfigParser()
        config.read(keys_path)

        self.client_id = config['SpotifyAPI']['client_id']
        self.client_secret = config['SpotifyAPI']['client_secret']
        self.username = config['SpotifyAPI']['username']
        self.redirectURI = config['SpotifyAPI']['redirect']



# Get Spotify Authentication
keys_path = "auth/spotify_keys.ini"
spotify_auth = SpotifyAuth(keys_path)

# Authenticate Spotify and get credentials manager as sp
client_credentials_manager = SpotifyClientCredentials(spotify_auth.client_id, spotify_auth.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_get_song_name(word):
    track_results = sp.search(q=word, type="track", limit = 50)
    # split message into words
    names = [e['name'] for e in track_results['tracks']['items']]
    # add space after name to get cleaner names
    names = [name + " " for name in names]
    print(names)
    starts_with = [name for name in names if name.lower().startswith(word.lower())]

    return starts_with

def get_message_songs(message):
    message_list = message.split(" ")

    hidden_message_songs = []
    for word in message_list:
        songs_list = search_get_song_name(word)
        print(songs_list)
        song = random.choice(songs_list)
        hidden_message_songs.append(song)

    print('HIDDEN MESSAGE')
    print(hidden_message_songs)

    return hidden_message_songs