import os
import requests
from cred_auth import api_key_vagalume

api_key = api_key_vagalume
letra_tmp = ''


def letra(mus):
    global letra_tmp
    musica, artista = mus.values()
    if musica in letra_tmp:
        return letra_tmp
    try:
        print(f"Pesquisando {musica.strip()} - {artista.strip()}...")
        resp_letra = requests.get(
            f'https://api.vagalume.com.br/search.php?art={artista}&mus={musica}&apikey={api_key}')
        resp_letra = resp_letra.json()
        letra_txt = resp_letra['mus'][0]['text']
    except Exception as inst:
        return f"Ocorreu um erro, ...tipo {type(inst)}"

    letra_tmp = '\n\n' + musica + '\n\n' + letra_txt + '\n\n'
    return letra_tmp


if __name__ == "__main__":
    while True:
        proxima = input('Aperte enter pra ver letra da musica atual ou escreva x pra sair: ')
        if proxima == '':
            os.system('cls')
            print(letra())
        elif proxima == 'x':
            break
