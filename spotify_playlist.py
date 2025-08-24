import spotipy
from spotipy import SpotifyOAuth

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = '0acae2fbe0274ea2bdd412a19f09410e',
                                                      client_secret = 'b5673e0810334dd2aa3fce8939ebd3a4',
                                                      redirect_uri = 'http://google.com/',
                                                        ))


def songs_list(url):
    song_list = []

    results = sp.playlist(url)
    for item in results['tracks']['items']:
        song_list.append(
        item['track']['name'] + ' - ' +
        item['track']['artists'][0]['name'])

    return song_list

