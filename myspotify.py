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
    track_properties = [{'song': e['name'],'artists': e['artists'],'album_cover': e['album']['images'][0]['url'],'id':e['id'],'word':word} for e in track_results['tracks']['items']]
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

    # filter search results for songs that match beginning word only
    filtered_track_properties = [song for song in track_properties if song['song'].lower().startswith(word.lower())]

    # print(track_properties)
        
    return filtered_track_properties

def get_features(filtered_track_properties):
    df = pd.DataFrame(filtered_track_properties)
    ids = list(df['id'])
    features  = sp.audio_features(ids)
    features = pd.DataFrame(features)
    df_master = df.merge(features, on="id")
    master_dict = df_master.to_dict(orient="records")

    return master_dict


def return_closest_song(master_dict, valence_input, energy_input, dance_input):
    # return song closest to slider values

    # scale 0-100 to 0 to 1

    closest_dict = min(
        master_dict,
        key=lambda d: (
            abs(d["valence"] - (float(valence_input)/100)) +
            abs(d["energy"] - (float(energy_input)/100)) +
            abs(d["danceability"] - (float(dance_input)/100))
        )
    )
    return closest_dict


def get_message_songs(message, valence_input, energy_input, dance_input):
    message_list = message.split(" ")
    message_list = [word+" " for word in message_list]

    # Initialize an empty DataFrame with the same columns as `song_df`
    songs_list_dict = []

    for word in message_list:
        # Retrieve songs for the current word and filter for first word matching the song
        search_results = search_get_song_name(word)  
        # Grab music features
        master_dict = get_features(search_results)

        # Get closest song to slider values
        song = return_closest_song(master_dict, valence_input, energy_input, dance_input)
        # Append the selected row to `hidden_message_songs
        print(song)
        songs_list_dict.append(song)

    print('HIDDEN MESSAGE')
    # print(song_list_dict)

    return songs_list_dict



