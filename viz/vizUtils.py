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


def lerp_gradient(colors, t):
    if not colors:
        raise ValueError("Colors list cannot be empty")

    if len(colors) == 1:
        return colors[0]

    # Clamp t to [0, 1]
    t = max(0.0, min(1.0, t))

    n = len(colors) - 1  # Number of segments
    scaled_t = t * n
    segment = int(scaled_t)

    # Handle edge case where t = 1.0
    if segment >= n:
        return colors[-1]

    # Get the two colors to interpolate between
    c1 = colors[segment]
    c2 = colors[segment + 1]

    # Local interpolation factor within this segment
    local_t = scaled_t - segment

    # Linear interpolation for each channel
    r = int(c1[0] + (c2[0] - c1[0]) * local_t)
    g = int(c1[1] + (c2[1] - c1[1]) * local_t)
    b = int(c1[2] + (c2[2] - c1[2]) * local_t)

    return (r, g, b)

import math
def easing(x,lifespan): # uses sqrt(x) to ease between 1 and 0
    if lifespan == 0:
        raise ValueError("Lifespan cannot be zero")
    if x <= 0:
        return 0
    if x >= lifespan:
        return 1
    sx = math.sqrt(x)
    sl = math.sqrt(lifespan)
    return sx/sl
def lerp_gradient_eased(x,lifespan,gradient):
    nx = easing(x,lifespan)
    grad = lerp_gradient(gradient,nx)
    return grad







