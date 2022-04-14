import threading
import time
from multiprocessing.connection import Listener, Client
import eel


def process_message(instance, msg):
    match msg[0]:
        case "games_played":
            instance.games_played = msg[1]
        case "reboot":
            instance.reboots = msg[1]


class Gui:
    games_played = 0
    reboots = 0
    tokens_earned = 0

    def __init__(self):
        pass

    def listen(self):
        address = ('localhost', 6000)  # family is deduced to be 'AF_INET'
        listener = Listener(address, authkey=b'?')
        conn = listener.accept()

        time.sleep(6)
        game_client = Client(('localhost', 6001), authkey=b'?')
        game_client.send('start')
        while True:
            msg = conn.recv()
            process_message(self, msg)
            if msg == 'close':
                conn.close()
                break
        listener.close()

    def initialize_gui(self):
        eel.init('web')
        listener = threading.Thread(target=self.listen)
        listener.start()
        eel.start('index.html', size=(300, 200))
