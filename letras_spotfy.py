import requests
from credencials import api_key_vagalume

api_key = api_key_vagalume  # Chave de api: https://auth.vagalume.com.br/
letra_tmp = ''


def letra(mus):
    global letra_tmp
    musica, artista = mus.values()
    if 'feat' in musica.lower():
        musica = musica[:musica.lower().find('(feat.')]
    artista = artista.replace('&', 'e')
    if musica in letra_tmp:
        return letra_tmp
    try:
        print(f"Pesquisando {musica} - {artista.strip()}...")
        resp_letra = requests.get(
            f'https://api.vagalume.com.br/search.php?art={artista.strip()}&mus={musica.strip()}&apikey={api_key}')
        resp_letra = resp_letra.json()
        letra_txt = resp_letra['mus'][0]['text']
    except Exception as inst:
        return f"Ocorreu um erro, ...tipo {type(inst)}"

    letra_tmp = '\n\n' + musica + '\n\n' + letra_txt + '\n\n'
    return letra_tmp


if __name__ == "__main__":
    from Spotify_py import SpotBot
    from credencials import spotify_credencials
    import os
    spotbot = SpotBot(spotify_credencials['user'],
                      spotify_credencials['scope'],
                      spotify_credencials['client_id'],
                      spotify_credencials['client_secret'],
                      spotify_credencials['redirect_uri'])
    while True:
        proxima = input('Aperte enter pra ver letra da musica atual ou escreva x pra sair: ')
        if proxima == '':
            os.system('cls')
            print(letra(spotbot.current()))
        elif proxima == 'x':
            break
