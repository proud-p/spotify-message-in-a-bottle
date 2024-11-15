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

# set up our landing page
@app.route('/')
def index():
	my_songs = get_message_songs(default_message)
	return render_template('index.html', songs=my_songs, hidden_message=default_message)

# only use this when posting data!
@app.route('/', methods=['POST'])
def index_post():
	message = request.form['message']
	my_songs = get_message_songs(message)
	return render_template('index.html', songs=my_songs, hidden_message=message)