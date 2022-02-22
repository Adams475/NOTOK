from timeit import default_timer as timer
from pytesseract import pytesseract as tess
from PIL import ImageGrab
import subprocess
import signal
import sys
import pyautogui
import time
import consts
import controller
import decisions
import utils

tess.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pyautogui.FAILSAFE = False
in_queue = True
in_game = False
got_into = True
composition = consts.yordles
games_played = -1
start_queue = 0
client_reboots = 0


def signal_handler(sig, frame):
    print('Games played: ' + str(games_played) + ', Client Reboots: ' + str(client_reboots))
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    while in_queue:
        if got_into:
            start_queue = timer()
            games_played += 1
            got_into = False
        if utils.elapsed_time(start_queue, 600):
            subprocess.call(["taskkill", "/F", "/IM", "LeagueClient.exe"])
            time.sleep(30)
            subprocess.call(['C:\\Riot Games\\League of Legends\\LeagueClient.exe'])
            time.sleep(60)
            controller.move_and_click(coord=(442, 198))
            controller.move_and_click(coord=(938, 396))
            controller.move_and_click(coord=(861, 839))
            start_queue = 0
            client_reboots += 1
            continue
        controller.move_and_click(consts.find_match)
        time.sleep(2)
        controller.move_and_click(consts.accept)
        time.sleep(2)
        controller.move_and_click(consts.ok)
        time.sleep(2)
        start = timer()
        health_count = 0
        while utils.league_is_running():
            start_queue = 0
            got_into = True
            img = ImageGrab.grab()
            if utils.elapsed_time(start, dur=10):
                if health_count % 10 == 0:
                    controller.move_and_click(bbox=consts.battle_stats)
                health_count += 1
                start = timer()
                health = utils.get_cnum(img, consts.hp)
                if decisions.check_quit(health):
                    break
            gold_check = utils.get_cnum(ImageGrab.grab(), consts.gold)
            # Not in an actionable state
            if gold_check == -1:
                cards = utils.get_cards(img)
                for choice in consts.card_choices:
                    if cards is not None and choice in cards:
                        controller.move_and_click(bbox=consts.cards[cards.index(choice)])
            # In an actionable state
            else:
                shop = utils.get_shop(img)
                for champ_name in shop:
                    if champ_name in composition:
                        controller.purchase(shop.index(champ_name))
                if utils.get_lvl(img) >= 6:
                    if gold_check >= 54:
                        controller.press_key('d')
                elif utils.get_lvl(img) == 5:
                    if gold_check >= 54:
                        j = int((gold_check - 50) / 4)
                        for i in range(j):
                            controller.press_key('f')
