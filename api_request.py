'''
APIRequest object gets Spotify data from Spotify API
'''

import requests
from math import ceil

class APIRequest:
    #
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = ''
        #headers used for all api requests
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token,
        }
        self.base_url = 'https://api.spotify.com/v1'

        self.refresh_token()

    def refresh_token(self):
        #gets access token given client id and client secret
        self.token = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            params={"grant_type":"client_credentials",
                'client_id':self.client_id,
                'client_secret':self.client_secret}
        ).json()['access_token']

        self.headers['Authorization'] = 'Bearer '+self.token


    def get_objects(self, id_list, type):
        if type not in ['tracks', 'audio-features', 'artists', 'albums']:
            print(f'Error: Object type <{type}> not supported.')
            return
        
        # api can return max of 20 albums, max of 50 for others
        if type == 'albums':
            id_max = 20
        else:
            id_max = 50

        object_list = []

        # gets json objects in chunks of id_max
        for i in range(ceil(len(id_list)/id_max)):
            track_id_slice = id_list[id_max*i:id_max*i+id_max]
            object_list += requests.get(f"{self.base_url}/{type}", headers=self.headers, params={'ids':','.join(track_id_slice)}).json()[type.replace('-','_')]

        # returns list of unaltered json objects
        return object_list
    
    def get_playlist_track_list(self, playlist_id, limit=50):
        track_info_list = []
        track_audio_list = []
        # limit for getting playlists tracks is 100, gets json objects in chunks of 100
        for i in range(int((limit - 1)/100 + 1)):
            # with each loop, if the limit hasn't been reached, get 100 objects
            # else, get the remainder
            mod_limit = 100 if limit >= 100*i else limit%100
            params = {'offset':100*i,'limit':mod_limit}
            tracks = requests.get(f"{self.base_url}/playlists/{playlist_id}/tracks",headers=self.headers,params=params).json()['items']

            # if track list is empty (ie there are no more tracks to get) break out of loop
            if not tracks:
                break

            # gets track ids from playlist tracks, uses those ids to get info and audio features
            track_ids = [track['track']['id'] for track in tracks]
            track_info = self.get_objects(track_ids, 'tracks')
            track_audio = self.get_objects(track_ids, 'audio-features')

            track_info_list += track_info
            track_audio_list += track_audio

            if 100*i + mod_limit >= limit:
                break

        return track_info_list, track_audio_list