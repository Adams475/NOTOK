import threading
from multiprocessing.connection import Listener
import eel


class Gui:
    test = "Unchanged"

    def __init__(self):
        pass

    def listen(self):
        address = ('localhost', 6000)  # family is deduced to be 'AF_INET'
        listener = Listener(address, authkey=b'?')
        conn = listener.accept()
        print('connection accepted from', listener.last_accepted)
        while True:
            msg = conn.recv()
            self.test = "Changed"
            if msg == 'close':
                conn.close()
                break
        listener.close()

    def initialize_gui(self):
        eel.init('web')
        listener = threading.Thread(target=self.listen)
        listener.start()
        while True:
            print(self.test)
        eel.start('index.html', size=(300, 200))
