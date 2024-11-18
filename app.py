from flask import Flask, render_template, request
from myspotify import get_message_songs

# app is a variable representing 
# our flask app
# __name__ is a python reserved 
# word
# telling Flask where our code
# lives - this goes directly into html
app = Flask(__name__)

default_message = 'CHICKEN NOODLE SOUP'
default_slider = 50

# set up our landing page
@app.route('/')
def index():
	my_songs = get_message_songs(default_message, valence_input=default_slider, energy_input=default_slider,dance_input=default_slider)

	return render_template('index.html', songs=my_songs, hidden_message=default_message, happy_sad_slider=default_slider, energy_slider =default_slider, danceability_slider=default_slider)

# only use this when posting data!
@app.route('/', methods=['POST'])
def index_post():
	message = request.form['message']
	valence_input = request.form['sad_happy_slider']
	energy_input = request.form['energy_slider']
	dance_input = request.form['danceability_slider']
	my_songs = get_message_songs(message, valence_input,energy_input,dance_input)

	return render_template('index.html', songs=my_songs, hidden_message=message, happy_sad_slider=valence_input, energy_slider =energy_input, danceability_slider=dance_input)