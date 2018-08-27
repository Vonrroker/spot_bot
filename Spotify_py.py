import os
from pprint import pformat
import spotipy
import spotipy.util as util


class SpotBot:
    def __init__(self, user_id, scope, client_id, client_secret, redirect_uri):
        self.user_id = user_id
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        try:
            token = util.prompt_for_user_token(self.user_id, self.scope, client_id=self.client_id,
                                               client_secret=self.client_secret,
                                               redirect_uri=self.redirect_uri)
            self.client = spotipy.Spotify(auth=token)
        except Exception:
            os.remove(f".cache-{self.user_id}")
            token = util.prompt_for_user_token(self.user_id, self.scope, client_id=self.client_id,
                                               client_secret=self.client_secret,
                                               redirect_uri=self.redirect_uri)
            self.client = spotipy.Spotify(auth=token)

    def playlist(self, playlist_id):
        playlist = self.client.user_playlist(self.user_id, playlist_id=playlist_id)

        return pformat([f"{x+1} - {playlist['tracks']['items'][x]['track']['name']}"
                        for x in range(len(playlist['tracks']['items']))])

    def add_song(self, tracks):
        try:
            if '?si=' in tracks:
                tracks = tracks[5:tracks.find('?si=')]
            else:
                retorno = self.client.search(tracks[5:], 1, 0, 'track')
                print(
                    f"{retorno['tracks']['items'][0]['name']} - {retorno['tracks']['items'][0]['album']['name']} - "
                    f"{retorno['tracks']['items'][0]['artists'][0]['name']}")
                tracks = retorno['tracks']['items'][0]['uri']
            tracks_ids = [tracks]
            self.client.user_playlist_add_tracks(self.user_id, playlist_id='1E8nC1fhAGsdNn2nRDSgGf', tracks=tracks_ids)
            info = self.client.track(tracks_ids[0])
            return f"{info['name']} - {info['artists'][0]['name']} adicionado com sucesso"
        except Exception:
            return f'Não foi possivel add a musica {tracks[5:]}'

    def skip(self):
        self.client.next_track()

    def play(self):
        self.client.start_playback()

    def stop(self):
        self.client.pause_playback()

    def volume(self, vol):
        if vol > 0 or vol < 100:
            self.client.volume(vol)
        else:
            print('volume invalido')
