'''
Spotify object classes provide easier access to data from the API.
Given a json object, each class gets necessary data as well as other attributes to help in further processing.
'''

class Track:
    # Track needs two json objects for necessary data
    def __init__(self, track_info_json, track_audio_json):
        self.id = track_info_json['id']
        self.data = {
            'id':track_info_json['id'],
            'name':track_info_json['name'],
            'album_id':track_info_json['album']['id'],
            'duration':track_info_json['duration_ms'],
            'explicit':track_info_json['explicit'],
            'danceability':track_audio_json['danceability'],
            'energy':track_audio_json['energy'],
            'key':track_audio_json['key'],
            'loudness':track_audio_json['loudness'],
            'mode':track_audio_json['mode'],
            'speechiness':track_audio_json['speechiness'],
            'acousticness':track_audio_json['acousticness'],
            'instrumentalness':track_audio_json['instrumentalness'],
            'liveness':track_audio_json['liveness'],
            'valence':track_audio_json['valence'],
            'tempo':track_audio_json['tempo'],
            'time_signature':track_audio_json['time_signature']
        }

        self.popularity = track_info_json['popularity']     # popularity included for insertion into playlist_tracks
        self.artist_ids = [a['id'] for a in track_info_json['artists']]     # list of artist ids to update artist_tracks, artists tables
        self.album_id = track_info_json['album']['id']      # album_id included for ease of access (already in data)


class Artist:
    def __init__(self, artist_json):
        self.id = artist_json['id']
        self.data = {
            'id':artist_json['id'],
            'name':artist_json['name'],
            'popularity':artist_json['popularity'],
            'followers':artist_json['followers']['total']
        }
    
        self.genres = artist_json['genres']     # list of genres to add to artist_genres table

class Album:
    def __init__(self, album_json):
        self.id = album_json['id']
        self.data = {
            'id':album_json['id'],
            'name':album_json['name'],
            'type':album_json['album_type'],
            'release_date':album_json['release_date']
        }

        # if album release date is not complete, then dummy dates are added
        # (probably need to rework this)
        if len(self.data['release_date']) == 4:
            self.data['release_date'] += '-01-01'

        elif len(self.data['release_date']) == 7:
            self.data['release_date'] += '-01'
