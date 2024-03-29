import time

import pyautogui
import pydirectinput
from PIL import ImageGrab
import consts
import controller
import main
import utils


def check_quit(health):
    if health == 0:
        controller.move_and_click(consts.exit_game)
        pyautogui.leftClick()
        time.sleep(1)
        pyautogui.mouseUp()
        time.sleep(0.5)
        pyautogui.mouseDown()
        controller.move_and_click(consts.exit_game)
        time.sleep(5)
        return True


def check_sell(index):
    img = ImageGrab.grab(bbox=consts.bench_chars_names[index])
    name = utils.get_ctext(img)
    if name not in main.composition:
        pydirectinput.press('e')
