"""OSC to Keypress
This example creates an OSC server (receives messages) and converts an "accelerometer" message into a keypress (down & up) event based on its length (magnitude).
"""

import argparse
import math
import keyboard
import vectormath as vmath


from pythonosc import dispatcher
from pythonosc import osc_server


def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))


def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError:
        pass


def press_key_handler(arg1, x, y, z):
    global is_pressed
    inputVector = vmath.Vector3(x, y, z)
    print(arg1, x, y, z, inputVector.length)
    if inputVector.length > 15 and not is_pressed:
        keyboard.send('space')
        is_pressed = True
    elif is_pressed:
        is_pressed = False


if __name__ == "__main__":
    is_pressed = False

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.0.171",
                        help="The ip to listen on")
    parser.add_argument("--port", type=int, default=9000,
                        help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/accelerometer", press_key_handler)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
