'''
SQLEngine encapsulates SQLAlchemy engine and personalizes functions for specific purposes.
'''

import pandas as pd
from sqlalchemy import create_engine, inspect

class SQLEngine:
    def __init__(self, database_url):
        try:
            self.engine = create_engine(database_url)
        except:
            print('Could not connect to SQL Database.')
            return
    
    # gets data from one column for specified table, default column is 'id'
    def get_column(self, table, column='id'):
        if table not in ['playlists','tracks','albums','artists']:
            print(f"Table name <{table}> not supported.")
            return
        else:
            return list(pd.read_sql(f"select id from {table}", self.engine)[column])
    
    # given a dict of pandas dataframes, inserts data into correct table
    def insert_table_data(self, df_dict):
        table_names = inspect(self.engine).get_table_names()
        with self.engine.connect() as con:
            for table in df_dict:
                if table not in table_names:
                    print(f"Table name <{table}> does not exist.")
                else:
                    
                    try:
                        # adds data to specific table, outputs number of rows added to table
                        df_dict[table].to_sql(table, con=con, if_exists='append', index=False)
                        print(f"Added {len(df_dict[table].index)} items to <{table}>.")
                    except:
                        # note, will fail to insert data into playlist_tracks' if playlist has already been updated
                        # might add functionality to prevent this later
                        print(f"Failed to insert data into <{table}>.")
                    

    # function to add a new playlist to the database
    # not called in driver object, used to manually add new playlists
    def add_playlist(self, playlist_id, name, type):
        df = pd.DataFrame(data=[[playlist_id, name, type]], columns=['id', 'name', 'type'])
        with self.engine.connect() as con:
            df.to_sql('playlists', con=con, if_exists='append', index=False)