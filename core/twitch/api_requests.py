import json
import requests
from core.framework import configuration


def get_twitch_headers():
	return {'Client-ID': 'q6batx0epp608isickayubi39itsckt', 'Accept': 'application/vnd.twitchtv.v5+json'}


def get_channel_id(channel_name=configuration.get_channel_name()):
	response = requests.get('https://api.twitch.tv/kraken/users?login=' + channel_name, headers=get_twitch_headers())
	return response.json()['users'][0]['_id']


def get_stream_category(channel_name=configuration.get_channel_name()):
	channel_id = get_channel_id(channel_name)
	response = requests.get('https://api.twitch.tv/kraken/channels/' + channel_id, headers=get_twitch_headers())
	return response.json()['game']
