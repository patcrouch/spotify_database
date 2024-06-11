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

        # new object lists get updated as neccessary if not already in db
        new_tracks = []
        new_artist_ids = set()
        new_album_ids = set()

        # data lists to contain row data to be added to respective table
        playlist_track_data_list = []
        tracks_data_list = []
        artists_data_list = []
        artist_tracks_data_list = []
        albums_data_list = []
        artist_genres_data_list = []

        # gets tracks and audio objects from api
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
                # adds data to artist_tracks table
                # note, if a track is new, its artist_track entry will also be new, regardless of whether the artist exists in the db
                # a track will never have new artists, but an artist may have new tracks
                artist_tracks_data_list.append({'track_id':track.id, 'artist_id':artist_id})
                if artist_id not in existing_artists:
                    new_artist_ids.add(artist_id)       # if the artist does not exist in db, add it to list for insertion later
            if track.album_id not in existing_albums:
                new_album_ids.add(track.album_id)   # if the album does not exist in db, add it to list for insertion later

        # new artists and albums added to respective data lists
        artist_objects = [Artist(artist) for artist in self.api_request.get_objects(list(new_artist_ids), 'artists')]
        for artist in artist_objects:
            # updates artists genres
            artists_data_list.append(artist.data)
            artist_genres_data_list += [{'artist_id':artist.id, 'genre':genre} for genre in artist.genres]

        album_objects = [Album(album) for album in self.api_request.get_objects(list(new_album_ids), 'albums')]
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

    # function that updates all playlists in the database while printing status 
    # this function will the primary function used to update the database
    def update_all_playlists(self, date=dt.date.today()):
        ids = self.sql_engine.get_column('playlists', 'id')
        names = self.sql_engine.get_column('playlists', 'name')
        playlist_dict = dict(zip(ids, names))

        for i, id in enumerate(playlist_dict):
            print(f"Updating '{playlist_dict[id]}'...")
            self.update_playlist(id, date)
            print(f"Updated '{playlist_dict[id]}'.")
            print(f"{i+1} of {len(playlist_dict)} playlists have been updated.\n")


    # given a list of tracks, adds artists to db if they don't exist
    # note, if read_playlists is working correctly, this function shouldn't be necessary since all artists should be updated automatically
    def add_artists_by_track(self, track_ids):
        # logic similar to read_playlists
        # loops through each track object, checks if the artists exist, adds data as necessary
        existing_artists = self.sql_engine.get_column('artists')
        track_info_json = self.api_request.get_objects(track_ids, 'tracks')
        tracks = [Track(track) for track in track_info_json]
        artist_tracks_data_list = []
        artists_data_list = []
        artist_genres_data_list = []
        artist_ids = set()
        for track in tracks:
            for artist_id in track.artist_ids:
                if artist_id not in existing_artists:
                    artist_tracks_data_list.append({'track_id':track.id, 'artist_id':artist_id})
                    artist_ids.add(artist_id)

        artist_objects = [Artist(artist) for artist in self.api_request.get_objects(list(artist_ids), 'artists')]
        for artist in artist_objects:
            artists_data_list.append(artist.data)
            artist_genres_data_list += [{'artist_id':artist.id, 'genre':genre} for genre in artist.genres]

        self.sql_engine.insert_table_data({
            'artists':pd.DataFrame(artists_data_list),
            'artist_tracks':pd.DataFrame(artist_tracks_data_list),
            'artist_genres':pd.DataFrame(artist_genres_data_list)
        })

    # given a list of artist ids, adds artists to db if they don't exist
    # note, if read_playlists is working correctly, this function shouldn't be necessary since all artists should be updated automatically
    def add_artists_by_id(self, artist_ids):
        existing_artists = self.sql_engine.get_column('artists')
        artists_data_list = []
        artist_genres_data_list = []

        artist_objects = [Artist(artist) for artist in self.api_request.get_objects(artist_ids, 'artists')]
        for artist in artist_objects:
            if artist.id not in existing_artists:
                artists_data_list.append(artist.data)
                artist_genres_data_list += [{'artist_id':artist.id, 'genre':genre} for genre in artist.genres]

        self.sql_engine.insert_table_data({
            'artists':pd.DataFrame(artists_data_list),
            'artist_genres':pd.DataFrame(artist_genres_data_list)
        })

    # given a list of album ids, adds album to db if they don't exist
    # note, if read_playlists is working correctly, this function shouldn't be necessary since all albums should be updated automatically
    def add_albums_by_id(self, album_ids):
        albums_data_list = []

        album_objects = [Album(album) for album in self.api_request.get_objects(list(album_ids), 'albums')]
        albums_data_list += [album.data for album in album_objects]

        self.sql_engine.insert_table_data({
            'albums':pd.DataFrame(albums_data_list)
        })