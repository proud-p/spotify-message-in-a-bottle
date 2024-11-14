# Spotify scopes (INCLUDE ugc-image-upload)
import configparser
import pandas as pd


class SpotifyAuth:
    def __init__(self,keys_path):
        config = configparser.ConfigParser()
        config.read(keys_path)

        self.client_id = config['SpotifyAPI']['client_id']
        self.client_secret = config['SpotifyAPI']['client_secret']
        self.username = config['SpotifyAPI']['username']
        self.redirectURI = config['SpotifyAPI']['redirect']


def spotify_tracks_to_df(track_results):

    def clean_artist(list_of_artists):
        just_names = [d['name'] for d in list_of_artists]
        results_string = " & ".join(just_names)

        return results_string
    

    df = pd.DataFrame(track_results['tracks']['items'])
    df['clean_artist_names'] = df['artists'].apply(lambda x: clean_artist(x))
    clean_df = df[['name','clean_artist_names']]
    clean_df = clean_df.rename(columns = {'clean_artist_names':'artists','name':'song'})

    return clean_df
