from flask import Flask, render_template, request
from stravalib import Client
import pymongo


app = Flask(__name__)
mc = pymongo.MongoClient()
db = mc['runpaw']
tokens = db['strava_tokens']


with open('redirect_uri.txt') as f:
    REDIRECT_URI = f.read().strip()
with open('.strava_client_secret') as f:
    STRAVA_CLIENT_SECRET = f.read().strip()
with open('.strava_client_id') as f:
    STRAVA_CLIENT_ID = f.read().strip()


def get_auth_url():
    """Get the Strava authorization URL."""
    client = Client()
    auth_url = client.authorization_url(
        client_id=STRAVA_CLIENT_ID,
        redirect_uri= REDIRECT_URI)
    return auth_url


AUTH_URL = get_auth_url()


@app.route('/')
def index():
    """Show the home page."""
    return render_template('index_2.html', auth_url=AUTH_URL)


@app.route('/authorization')
def authorize():
    code = request.args.get('code')
    client = Client()
    access_token = client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID,
						  client_secret=STRAVA_CLIENT_SECRET,
						  code=code)
    tokens.insert_one({'token': access_token})
    return render_template('success.html', token=access_token)
