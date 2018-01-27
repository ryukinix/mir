#!/usr/bin/python
# coding=utf-8

import subprocess
import os

# third-library
import serial
from serial.tools.list_ports import comports as list_ports
from serial.serialutil import SerialException
from pymouse import PyMouse
from pykeyboard import PyKeyboard
# self-package
import mir.keys as keys
import mir.x as X

m = PyMouse()
k = PyKeyboard()
BAUDRATE = 9600


def toggle_monitor():
    p = subprocess.Popen(["/usr/bin/xset", "-q"],
                         stdout=subprocess.PIPE)
    out, err = p.communicate()

    result = out.decode("utf-8")

    if result.find("Monitor is On") >= 0:
        os.system("xset -display :0.0 dpms force off")
    elif result.find("Monitor is Off") >= 0:
        os.system("xset -display :0.0 dpms force on")
    else:
        print(" toggle_monitor: Error: {!r} ".format(err), end='')


def connect(port):
    "Connect the serial port and return connection"
    return serial.Serial(port, BAUDRATE)


def stream_connection(conn):
    "Make a stream of signals based on the conn (serial connection)"
    while True:
        yield int(conn.readline().decode('utf-8').strip(), 16)


def interpreter(signal):
    "Given a signal 8-digit hex encoded integer, make a action"
    print("SIGNAL: {:08X}".format(signal), end='')

    if signal == keys.VOL_UP:
        k.tap_key(X.VOL_DOWN)
    elif signal == keys.VOL_DOWN:
        k.tap_key(X.VOL_UP)
    elif signal == keys.MUTE:
        k.tap_key(X.MUTE)
    elif signal == keys.RED:
        k.press_key(k.alt_key)
        k.tap_key(k.function_keys[4])
        k.release_key(k.alt_key)
    elif signal == keys.CH_UP:
        k.tap_key(X.NEXT_SONG)
    elif signal == keys.CH_DOWN:
        k.tap_key(X.PREVIOUS_SONG)
    elif signal == keys.CONFIRM:
        k.tap_key(X.PLAY_PAUSE)
    elif signal == keys.IBUTTON:
        subprocess.Popen("rhythmbox")
    elif signal == keys.GUIDE:
        subprocess.Popen("spotify")
    elif signal == keys.YELLOW:
        k.tap_key(X.REBOOT_SESSION)
    elif signal == keys.SKY:
        toggle_monitor()
    elif signal == keys.UP:
        k.tap_key("Up")
    elif signal == keys.DOWN:
        k.tap_key("Down")
    elif signal == keys.LEFT:
        k.tap_key("Left")
    elif signal == keys.RIGHT:
        k.tap_key("Right")
    elif signal == keys.PLUS:
        k.tap_key("Return")
    elif signal == keys.INFO:
        k.tap_key(" ")
    elif signal == keys.MENU:
        k.press_key(k.shift_l_key)
        k.tap_key('Tab')
        k.release_key(k.shift_l_key)
    elif signal == keys.MATRIX:
        k.tap_key('Tab')
    else:
        print(" - Ignored.")
        return
    print(" - Action made.")


def main():
    "Main procedure of this fucking program"
    ports = list_ports()
    if not ports:
        print("None device attached. Review the cables.")
        return
    port = ports[0]
    conn = connect(port.device)
    print("Connected at {}".format(port.device))
    stream = stream_connection(conn)
    print("Streaming started.")
    for signal in stream:
        interpreter(signal)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutdown. Bye!")
    except SerialException:
        print("Device unplugged. Shutdown.")
