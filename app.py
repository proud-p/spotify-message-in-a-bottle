from flask import Flask, render_template, request
from myspotify import get_message_songs, create_playlist

app = Flask(__name__)

default_message = 'CHICKEN NOODLE SOUP'
default_slider = 50

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Default behavior for GET
        my_songs = get_message_songs(default_message, valence_input=default_slider, energy_input=default_slider, dance_input=default_slider)
        return render_template('index.html', songs=my_songs, hidden_message=default_message, happy_sad_slider=default_slider, energy_slider=default_slider, danceability_slider=default_slider)

    # Handle POST request
    message = request.form['message']
    valence_input = int(request.form['sad_happy_slider'])
    energy_input = int(request.form['energy_slider'])
    dance_input = int(request.form['danceability_slider'])
    action = request.form['action']  # Determine which button was pressed

    if action == "submit":
        # Handle Submit button
        my_songs = get_message_songs(message, valence_input, energy_input, dance_input)
        return render_template('index.html', songs=my_songs, hidden_message=message, happy_sad_slider=valence_input, energy_slider=energy_input, danceability_slider=dance_input)

    elif action == "create_playlist":
        # Handle Create Playlist button
        my_songs = get_message_songs(message, valence_input, energy_input, dance_input)
        playlist_id = create_playlist(my_songs)
        return render_template('index.html', songs=my_songs, hidden_message=message, happy_sad_slider=valence_input, energy_slider=energy_input, danceability_slider=dance_input, playlist_url=f"https://open.spotify.com/playlist/{playlist_id}")
