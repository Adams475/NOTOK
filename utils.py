import psutil
from PIL import ImageEnhance, ImageOps
import consts
import pytesseract as tess
from timeit import default_timer as timer


# Gets text from a cropped image (Must be a line of text - no paragraphs)
def get_ctext(img, area=None):
    if area is None:
        crop = img
    else:
        crop = img.crop(area)
    crop = correct_text(crop)
    crop.save("Test.png")
    text = tess.image_to_string(crop, lang='eng', config='--psm 7')
    if text is not None:
        text = text[0:text.find('\n')]
    return text


# Gets a number from a cropped image
def get_cnum(img, area):
    text = get_ctext(img, area)
    try:
        return int(text)
    except ValueError:
        return -1


# Attempts to make image more clear for tesseract
def correct_text(img):
    img = img.convert('L')
    img = ImageOps.invert(img)
    enhancer = ImageEnhance.Contrast(img)
    im_output = enhancer.enhance(2.0)
    im_output.save('more-contrast-image.png')
    return im_output


# Gets all names of champions in the shop
def get_shop(img):
    names = []
    for unit in consts.shop_names:
        names.append(get_ctext(img, unit))
    return names


# Checks if League game client is running
def league_is_running():
    for proc in psutil.process_iter():
        try:
            process_name = proc.name()
            if process_name == "League of Legends.exe":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            print("err")
    return False


# Simple elapsed time function
def elapsed_time(start_time, dur):
    curr = timer()
    if curr - start_time >= dur:
        return True


# Wrappers
def get_cards(img):
    text = []
    for card in consts.cards:
        text.append(get_ctext(img, card))
    return text


def get_gold(img):
    return get_ctext(img, consts.gold)


def get_time(img):
    return get_ctext(img, consts.time)


def get_stage(img):
    return get_ctext(img, consts.stage)


def get_exp(img):
    return get_ctext(img, consts.exp)


def get_lvl(img):
    return get_cnum(img, consts.level)


