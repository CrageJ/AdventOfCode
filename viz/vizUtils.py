import utils
from utils import get_root_folder
from PIL import Image
from collections import defaultdict

DEFAULT_COLOUR = (125,125,125)
loaded_character_dictionary = None
def get_alphabet():
    global loaded_character_dictionary
    if loaded_character_dictionary:
        return loaded_character_dictionary
    curr = get_root_folder()
    curr = curr / "viz" / "assets"
    img = Image.open(curr/"pixalphabet.pgm")
    chars = "abcdefghijklmnopqrstuvwxyz0123456789.,\"'?!_()+-/\:;@{}*^ &%$#~|<>`="
    px=img.load()
    lookup = {}
    for index,char in enumerate(chars):
        lx = index*6
        rx = index*6+5

        # Extract the 6px-wide slice manually
        slice_pixels = [
            [px[x, y] for x in range(lx, rx)]
            for y in range(5)
        ]

        lookup[char] = slice_pixels

    dict = defaultdict(lambda:lookup[" "])
    for k,v in lookup.items():
        dict[k] = v
    loaded_character_dictionary = dict
    return dict

def alpha_to_array_img(char_array,char_colours,background_colour=None,spacing=1):
    if not background_colour:
        background_colour = -1
    m,n = len(char_array),len(char_array[0])
    bigm,bign = (5+spacing)*m,(5+spacing)*n
    alphabet = get_alphabet()
    canvas = [[background_colour for x in range(bign)] for y in range(bigm)]
    for yb in range(bigm):
        for xb in range(bign):
            x,y = xb//(5+spacing),yb//(5+spacing)
            posx,posy = xb - x*(5+spacing),yb-y*(5+spacing)
            if 5>posx>=0 and 5>posy>=0:
                char = char_array[y][x]
                char_colour = char_colours[y][x]
                char_isFilled = alphabet[char][posy][posx] ==0
                canvas[yb][xb] = char_colour if char_isFilled else background_colour

    canvas = [[background_colour]+row for row in canvas]
    canvas = [[background_colour]*(bign+1)] + canvas
    return canvas








