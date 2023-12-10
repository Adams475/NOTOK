import os
import random
from timeit import default_timer as timer
from pytesseract import pytesseract as tess
from multiprocessing.connection import Client, Listener
from PIL import ImageGrab
import multiprocessing
import signal
import sys
import pyautogui
import threading
import time
import interface
import consts
import controller
import decisions
import utils

tess.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pyautogui.FAILSAFE = False
in_queue = True
in_game = False
got_into = True
composition = consts.kda
games_played = -1
start_queue = 0
client_reboots = 0
gui_client = None
start_main = False


def listen(pid):
    address = (consts.local_connection, consts.game_port)  # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey=b'?')
    conn = listener.accept()
    while True:
        msg = conn.recv()
        if msg == 'start':
            global start_main
            start_main = True
        if msg == 'close':
            gui_client.send('close')
            os.kill(pid, signal.SIGTERM)
            conn.close()
            break
    listener.close()


def spawn_child(target):
    child = multiprocessing.Process(target=target)
    child.start()


def signal_handler(sig, frame):
    print('Games played: ' + str(games_played) + ', Client Reboots: ' + str(client_reboots))
    gui_client.send('close')
    gui_client.close()
    sys.exit(0)


if __name__ == '__main__':
    spawn_child(interface.Gui().initialize_gui)
    gui_client = Client((consts.local_connection, consts.gui_port), authkey=b'?')
    gui_client.send(consts.open_connection)
    gui_client.send(os.getpid())
    signal.signal(signal.SIGINT, signal_handler)
    a = {os.getpid()}
    listen_thread = threading.Thread(target=listen, args=a)
    listen_thread.start()

    while not start_main:
        pass

    while in_queue:
        if got_into:
            start_queue = timer()
            games_played += 1
            got_into = False
        if utils.elapsed_time(start_queue, 600):
            utils.reboot()
            got_into = True
            client_reboots += 1
            continue
        controller.accept_queue()
        health_check = timer()
        time_collect = timer()
        turn_start = -1
        while utils.league_is_running():
            # Used for weird mouse shenanigans
            pyautogui.leftClick()
            pyautogui.leftClick()
            start_queue = 0
            got_into = True
            img = ImageGrab.grab()
            gold = utils.get_cnum(ImageGrab.grab(), consts.gold)
            if utils.elapsed_time(health_check, dur=5):
                health_check = timer()
                health = utils.get_cnum(img, consts.hp)
                if health == -1:
                    controller.move_and_click(bbox=consts.battle_stats)
                    controller.move_and_click(bbox=consts.battle_stats, btn='r')
                    time.sleep(0.5)
                    health = utils.get_cnum(img, consts.hp)
                if decisions.check_quit(health):
                    break
            if gold != -1:  # Runs multiple times per planning phase
                level = utils.get_lvl(img)
                for i in range(5):
                    img = ImageGrab.grab()
                    shop = utils.get_shop(img)
                    for champ_name in shop:
                        if champ_name in composition:
                            controller.purchase(shop.index(champ_name))
                if level >= 4:
                    r_roll = random.randint(0, 1)
                    r_level = random.randint(0, 1)
                    if (r_roll * 6) > (r_level * level):
                        if gold > 30:
                            controller.press_key('d')
                    else:
                        j = int((gold - 50) / 4)
                        for i in range(j):
                            controller.press_key('f')
            if utils.elapsed_time(time_collect, 30 and gold != -1):
                for point in consts.board_locs:
                    controller.move_and_click(point, btn='r')
                    time.sleep(2)
                time_collect = timer()
                controller.move_and_click(consts.home, btn='r')
