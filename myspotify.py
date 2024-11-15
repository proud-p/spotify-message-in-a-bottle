import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import configparser
import pandas as pd
import numpy as np

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
    track_properties = [{'song': e['name'],'artists': e['artists'],'album_cover': e['album']['images'][0]['url']} for e in track_results['tracks']['items']]
    # print(track_properties)

    # clean artist names
    for track in track_properties:
        track_artists = track['artists']

        artist_names = []
        for i in range(len(track_artists)):
            name = track_artists[i]['name']
            artist_names.append(name)

        clean_artist_names = " & ".join(artist_names)
        # replace clean artists names single string back into artist
        track['artists'] = clean_artist_names

    # print(track_properties)
        
    return track_properties


def get_message_songs(message):
    message_list = message.split(" ")
    message_list = [word+" " for word in message_list]

    # Initialize an empty DataFrame with the same columns as `song_df`
    songs_list_dict = []

    for word in message_list:
        # Retrieve songs for the current word
        search_results = search_get_song_name(word)  # Ensure this function returns a DataFrame

        # filter search results for songs that match beginning word only
        filtered_search_results = [song for song in search_results if song['song'].lower().startswith(word.lower())]

        # Get a random index from `song_df`
        song = random.choice(filtered_search_results)
        # Append the selected row to `hidden_message_songs
        print(song)
        songs_list_dict.append(song)

    print('HIDDEN MESSAGE')
    # print(song_list_dict)

    return songs_list_dict



