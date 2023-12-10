import random
import time
import pyautogui
import consts
import pydirectinput


def purchase(index):
    move_and_click(bbox=consts.shop_names[index])


def press_key(key):
    pydirectinput.press(key)


def move_and_click(coord=None, bbox=None, duration=None, btn=None):
    dur = duration
    if dur is None:
        dur = 0.2
    if bbox is None:
        x = coord[0]
        y = coord[1]
    else:
        x = random.randint(bbox[0] + 15, bbox[2] - 1)
        y = random.randint(bbox[1] + 1, bbox[3] - 1)
    r_dur = random.randint(2, 10)
    r_dur = r_dur / 10
    pyautogui.moveTo(x, y, duration=r_dur, tween=pyautogui.easeInOutQuad)
    if btn == 'r':
        pyautogui.rightClick()
        pyautogui.doubleClick(interval=1)
        pyautogui.doubleClick(interval=dur)
    else:
        pyautogui.doubleClick()
        pyautogui.doubleClick()
    pyautogui.mouseDown()
    pyautogui.mouseUp()


def accept_queue():
    move_and_click(consts.find_match)
    time.sleep(2)
    move_and_click(consts.accept)
    time.sleep(2)
    move_and_click(consts.ok)
    time.sleep(2)
