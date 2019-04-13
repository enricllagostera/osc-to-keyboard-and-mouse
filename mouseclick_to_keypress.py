"""Mouse to Keypress
This very short script converts from a mouse click to a keypress (down & up) of the 'Space' key.
"""

import keyboard
import mouse


def pressKey():
    keyboard.send('space')


mouse.on_click(pressKey)

keyboard.wait()
