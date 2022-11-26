import pandas as pd
import spotipy
import pandas as pd
import numpy as np

def get_spotify_ranking(client_id, client_secret):
    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language='ja')

    weekly_top_playlist_ids_dict = dict(
        Japan='37i9dQZEVXbKqiTGXuCOsB',  # 日本
    )

    playlist = sp.playlist(playlist_id='37i9dQZEVXbKqiTGXuCOsB', market='JP')
    tracks = playlist['tracks']['items'][:3]
    tracks_df = pd.DataFrame(np.zeros((3, 2)), columns=['title', 'uri'])
    for i, track in enumerate(tracks):
        idx = (3) + i
        track_info = track['track']
        tracks_df.loc[idx, 'title'] = track_info['name']
        tracks_df.loc[idx, 'uri'] = track_info['uri'].replace('spotify:track:', '')

    title = tracks_df['title'].to_list()
    uri = tracks_df['uri'].to_list()
    for u in range(3,6):
        uri[u] = 'https://open.spotify.com/track/' + uri[u]
    del title[:3]
    del uri[:3]
    return title, uri


