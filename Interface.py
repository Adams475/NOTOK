from multiprocessing.connection import Listener, Client
import threading
import eel
import psutil

import consts
import main


class Gui:

    def __init__(self):
        self.suspended = False
        self.main_process = None
        self.games_played = 0
        self.reboots = 0
        self.tokens_earned = 0
        self.game_client = None

    def initialize_gui(self):
        eel.init('web')
        listener = threading.Thread(target=self.listen)
        listener.start()
        while self.game_client is None:
            pass
        global gui_instance
        gui_instance = self
        eel.start('index.html', size=(500, 500))

    def listen(self):
        address = (consts.local_connection, consts.gui_port)  # family is deduced to be 'AF_INET'
        listener = Listener(address, authkey=b'?')
        conn = listener.accept()

        while True:
            msg = conn.recv()
            if msg == consts.open_connection:
                self.game_client = Client((consts.local_connection, consts.game_port), authkey=b'?')
                break

        while True:
            msg = conn.recv()
            self.process_message(msg)
            if msg == 'close':
                self.game_client.send("close")
                conn.close()
                break
        listener.close()

    def process_message(self, msg):
        print(msg[0])
        match msg[0]:
            case "games_played":
                self.games_played = msg[1]
            case "reboot":
                self.reboots = msg[1]
            case "pid":
                print("got pid")
                self.main_process = psutil.Process(msg[1])

    def pause(self):
        if not self.suspended:
            self.main_process.suspend()
            self.suspended = True
        else:
            self.main_process.resume()
            self.suspended = False


gui_instance = Gui()  # Dummy initialization


@eel.expose
def pause():
    gui_instance.pause()


@eel.expose
def communicate(arg):
    gui_instance.game_client.send(arg)
