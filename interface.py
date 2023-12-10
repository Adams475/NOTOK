from multiprocessing.connection import Listener, Client
import threading
import eel
import psutil
import consts


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
        address = (consts.local_connection, consts.gui_port)
        listener = Listener(address, authkey=b'?')
        conn = listener.accept()

        # Wait to receive initial connection from game client
        while True:
            msg = conn.recv()
            if msg == consts.open_connection:
                self.game_client = Client((consts.local_connection, consts.game_port), authkey=b'?')
                break

        # Process messages from game client
        while True:
            msg = conn.recv()
            if msg == 'close':
                eel.browser_exit()
                conn.close()
                break
            else:
                self.process_message(msg)

        listener.close()

    # Process messages from either eel or game client
    def process_message(self, msg):
        match msg:
            case "start":
                self.game_client.send(msg)
            case "games_played":
                self.games_played = msg
            case "reboot":
                self.reboots = msg
            case "pause":
                gui_instance.pause()
            case _:
                self.main_process = psutil.Process(msg)

    def pause(self):
        if not self.suspended:
            self.main_process.suspend()
            self.suspended = True
        else:
            self.main_process.resume()
            self.suspended = False


gui_instance = Gui()


@eel.expose
def communicate(arg):
    if arg == "exit":
        gui_instance.game_client.send("close")
    else:
        gui_instance.process_message(arg)
