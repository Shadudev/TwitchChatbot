import json
import requests
from core.framework import configuration


def get_stream_category():
	twitch_headers = {'Client-ID': 'q6batx0epp608isickayubi39itsckt', 'Accept': 'application/vnd.twitchtv.v5+json'}
	response = requests.get('https://api.twitch.tv/kraken/users?login=' + configuration.get_channel_name(), headers=twitch_headers)
	channel_id = response.json()['users'][0]['_id']
	response = requests.get('https://api.twitch.tv/kraken/channels/' + channel_id, headers=twitch_headers)
	return response.json()['game']


def get_channel_id(channel_name):
	twitch_headers = {'Client-ID': 'q6batx0epp608isickayubi39itsckt', 'Accept': 'application/vnd.twitchtv.v5+json'}
	response = requests.get('https://api.twitch.tv/kraken/users?login=' + configuration.get_channel_name(), headers=twitch_headers)
	return response.json()['users'][0]['_id']