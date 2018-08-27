import telepot
from telepot.loop import MessageLoop
from Spotify_py import SpotBot
from credencials import *

bot = telepot.Bot(telegram['token'])


spotbot = SpotBot(spotify_credencials['user'],
                  spotify_credencials['scope'],
                  spotify_credencials['client_id'],
                  spotify_credencials['client_secret'],
                  spotify_credencials['redirect_uri'])

skip = 0
users = []


def handle(msg):
    if msg['text'] == '/playlist':
        print(f"from: {msg['chat']['id']}, Msg: {msg['text']}")
        resp_playlist = spotbot.playlist(playlist_ids['spotbot_py'])
        print(f"Resposta: {resp_playlist}\n")
        bot.sendMessage(msg['chat']['id'], resp_playlist)
    elif msg['text'][:4] == '/add' and msg['text'][4:] != '':
        print(f"from: {msg['chat']['id']}, Msg: {msg['text']}")
        resp_add = spotbot.add_song(msg['text'])
        print(f"Resposta: {resp_add}\n")
        bot.sendMessage(msg['chat']['id'], resp_add)
    elif msg['text'] == '/skip':
        print(f"from: {msg['chat']['id']}, Msg: {msg['text']}")
        global users
        if msg['chat']['id'] not in users:
            users.append(msg['chat']['id'])
            global skip
            skip += 1
            if skip == 5:
                spotbot.skip()
                resp_skip = f'{skip}/5 música pulada\n'
                print(f"Resposta: {resp_skip}")
                bot.sendMessage(msg['chat']['id'], resp_skip)
                skip = 0
                users = []
            else:
                resp_skip = f'{skip}/5'
                print(f"Resposta: {resp_skip}\n")
                bot.sendMessage(msg['chat']['id'], resp_skip)
        else:
            resp_skip = 'Você so pode pedir pra pular uma vez'
            print(f"Resposta: {resp_skip}\n")
            bot.sendMessage(msg['chat']['id'], resp_skip)
    elif msg['text'] == '/play':
        print(f"from: {msg['chat']['id']}, Msg: {msg['text']}")
        spotbot.play()
        print(f"Resposta: Iniciando musica\n")
        bot.sendMessage(msg['chat']['id'], 'Iniciando musica')
    elif msg['text'] == '/stop':
        print(f"from: {msg['chat']['id']}, Msg: {msg['text']}")
        print(f"Resposta: Pausando musica\n")
        spotbot.stop()
        bot.sendMessage(msg['chat']['id'], 'Pausando musica')
    elif msg['text'][:4] == '/vol' and msg['text'][4:] != '':
        print(f"from: {msg['chat']['id']}, Msg: {msg['text']}")
        try:
            v = int(msg['text'][5:].replace(' ',''))
            if 0 <= v <= 100:
                spotbot.volume(v)
                print(f'Aumentando volume para {v}')
            else:
                print(f'Volume "{v}" invalido, escolha uma valor entre 0 e 100')
                bot.sendMessage(msg['chat']['id'], f'Volume {v} invalido, escolha uma valor entre 0 e 100')
        except ValueError:
            print(f"Volume {msg['text'][5:]} invalido, escolha uma valor entre 0 e 100")
            bot.sendMessage(msg['chat']['id'], f"Volume {msg['text'][5:]} invalido, escolha uma valor entre 0 e 100")
    else:
        print(f"from: {msg['chat']['id']}, Msg: {msg['text']}")
        print('Resposta: Comandos\n')
        bot.sendMessage(msg['chat']['id'], 'Por favor utilize um dos comandos disponiveis:'
                                           '\n/add "link ou nome da música"'
                                           '    \nPara add uma musica'
                                           '\n/playlist'
                                           '\n    Para ver a playlist'
                                           '\n/skip'
                                           '\n    Para pular a musica'
                                           '\n/vol "volume entre 0 e 100"'
                                           '\n/play'
                                           '\n/stop')


MessageLoop(bot, handle).run_as_thread()

while True:
    pass
