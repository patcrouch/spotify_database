'''
Driver class contains the main logic to update the Spotify database
Uses reques, engine, and object classes
'''

from api_request import APIRequest
from sql_engine import SQLEngine
from spotify_objects import Track, Artist, Album
import pandas as pd
import datetime as dt

class Driver:
    def __init__(self, database_url,client_id, client_secret):
        self.api_request = APIRequest(client_id, client_secret)
        self.sql_engine = SQLEngine(database_url)

    def update_playlist(self, playlist_id, date=dt.date.today()):
        # gets existing track, artist, and album ids to prevent duplicate entries
        existing_tracks = self.sql_engine.get_column('tracks')
        existing_artists = self.sql_engine.get_column('artists')
        existing_albums = self.sql_engine.get_column('albums')
        new_tracks = []
        new_artist_ids = []
        new_album_ids = []

        # data lists to contain row data to be added to respective table
        playlist_track_data_list = []
        tracks_data_list = []
        artists_data_list = []
        artist_tracks_data_list = []
        albums_data_list = []
        artist_genres_data_list = []

        playlist_tracks_info, playlist_tracks_audio = self.api_request.get_playlist_track_list(playlist_id)

        for track_info_json, track_audio_json in zip(playlist_tracks_info, playlist_tracks_audio):
            # for each track json object from the playlist, create track object
            track = Track(track_info_json, track_audio_json)

            # adds relevant data to playlist_tracks
            playlist_track_data_list.append({
                'playlist_id':playlist_id,
                'track_id':track.id,
                'date':date,
                'popularity':track.popularity
            })

            # adds to new tracks if row in track doesn't exist yet
            if track.id not in existing_tracks:
                new_tracks.append(track)
            
        for track in new_tracks:
            # for each new track, add data to tracks list, then check if the artists and album exist in database
            tracks_data_list.append(track.data)
            for artist_id in track.artist_ids:
                artist_tracks_data_list.append({'track_id':track.id, 'artist_id':artist_id})
                if artist_id not in existing_artists:
                    new_artist_ids.append(artist_id)
            if track.album_id not in existing_albums:
                new_album_ids.append(track.album_id)

        # prevents duplication of new artists
        new_artist_ids = list(pd.Series(new_artist_ids).unique())
        new_album_ids = list(pd.Series(new_album_ids).unique())

        # new artists and albums added to respective tables
        artist_objects = [Artist(artist) for artist in self.api_request.get_objects(new_artist_ids, 'artists')]
        for artist in artist_objects:
            # updates artists genres
            artists_data_list.append(artist.data)
            artist_genres_data_list += [{'artist_id':artist.id, 'genre':genre} for genre in artist.genres]

        album_objects = [Album(album) for album in self.api_request.get_objects(new_album_ids, 'albums')]
        albums_data_list += [album.data for album in album_objects]

        # once all data is received, add data to the database
        self.sql_engine.insert_table_data({
            'playlist_tracks':pd.DataFrame(playlist_track_data_list),
            'tracks':pd.DataFrame(tracks_data_list),
            'artists':pd.DataFrame(artists_data_list),
            'artist_tracks':pd.DataFrame(artist_tracks_data_list),
            'albums':pd.DataFrame(albums_data_list),
            'artist_genres':pd.DataFrame(artist_genres_data_list)
        })

        print(f'Updated <{playlist_id}>.')