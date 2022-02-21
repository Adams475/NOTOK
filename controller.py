import random
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
    rdur = random.randint(2, 10)
    rdur = rdur / 10
    pyautogui.moveTo(x, y, duration=rdur, tween=pyautogui.easeInOutQuad)
    if btn == 'r':
        pyautogui.rightClick()
    else:
        pyautogui.doubleClick(interval=dur)
    pyautogui.mouseUp()

