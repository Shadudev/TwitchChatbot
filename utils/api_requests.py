import json
import requests
from utils import configuration


def get_stream_category():
	twitch_headers = {'Client-ID': 'q6batx0epp608isickayubi39itsckt', 'Accept': 'application/vnd.twitchtv.v5+json'}
	response = requests.get('https://api.twitch.tv/kraken/users?login=' + configuration.CONNECTION_PARAMETERS['channel'], headers=twitch_headers)
	channel_id = response.json()['users'][0]['_id']
	response = requests.get('https://api.twitch.tv/kraken/channels/' + channel_id, headers=twitch_headers)
	return response.json()['game']
