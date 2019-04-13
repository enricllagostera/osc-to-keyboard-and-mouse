import sys
import argparse
import math
import keyboard
import vectormath as vmath
import PySimpleGUI as sg
import asyncio

from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher


async def loop():
    global transport
    global window
    # i = 0
    while(True):
        # i += 1
        # print(f"Loop {i}")
        event, values = window.Read(timeout=5)
        if event != '__TIMEOUT__':
            print(event, values)
        if event is None or event == 'Exit':
            break
        if event == '_CONNECT_':
            dispatcher = Dispatcher()
            dispatcher.map(values['_ADDRESS_'], press_key_handler)
            window.FindElement('_CONNECT_').Update(disabled=True)
            # server setup logic
            server = AsyncIOOSCUDPServer((values['_IP_'], int(
                values['_PORT_'])), dispatcher, asyncio.get_event_loop())
            # Create datagram endpoint and start serving
            transport, protocol = await server.create_serve_endpoint()
        await asyncio.sleep(0.005)


async def init_main():
    await loop()  # Enter main loop of program
    # transport.close()  # Clean up serve endpoint


def filter_handler(address, *args):
    global window
    print(f"{address}: {args}")
    window.FindElement('_DEBUG_').Update(
        f'{address} {args}\r\n', append=True)


def press_key_handler(address, *args):
    global is_pressed
    global window
    inputVector = vmath.Vector3(args[0], args[1], args[2])
    window.FindElement('_DEBUG_').Update(
        f'{address} {inputVector.length}\r\n', append=True)
    # print(arg1, x, y, z, inputVector.length)
    if inputVector.length > 15 and not is_pressed:
        keyboard.send('space')
        is_pressed = True
    elif is_pressed:
        is_pressed = False


# Window layout
layout = [
    [sg.Text('OSC IP:', size=(12, 1)),
        sg.Input(
        '192.168.0.171', key='_IP_', do_not_clear=True)],
    [sg.Text(
        'OSC Port:', size=(12, 1)), sg.Input('9000', key='_PORT_', do_not_clear=True)],
    [sg.Text('OSC Address:', size=(12, 1)), sg.Input(
        '/accelerometer', key='_ADDRESS_', do_not_clear=True)],
    [sg.Button('Connect', size=(12, 1), key='_CONNECT_', disabled=False)],
    [sg.Multiline('', key='_DEBUG_',
                  do_not_clear=True, size=(60, 8), change_submits=False,
                  enable_events=False, autoscroll=True, focus=False)],
    [sg.Button('Exit', size=(12, 1))]]

window = sg.Window('OSC to Keypress', layout=layout)
is_pressed = False

asyncio.run(init_main())

window.Close()
