#!/usr/bin/python
# coding=utf-8


# third-library
import serial
from serial.tools.list_ports import comports as list_ports
from pymouse import PyMouse
from pykeyboard import PyKeyboard

m = PyMouse()
k = PyKeyboard()

# self-package
import mir.keys as keys
import mir.x as X

BAUDRATE = 9600


def connect(port):
    "Connect the serial port and return connection"
    return serial.Serial(port, BAUDRATE)


def stream_connection(conn):
    "Make a stream of signals based on the conn (serial connection)"
    while True:
        yield int(conn.readline().decode('utf-8').strip(), 16)


def interpreter(signal):
    "Given a signal 8-digit hex encoded integer, make a action"
    print("SIGNAL: {:08X}".format(signal))

    if signal == keys.VOL_UP:
        k.tap_key(X.VOL_DOWN)
    elif signal == keys.VOL_DOWN:
        k.tap_key(X.VOL_UP)
    elif signal == keys.MUTE:
        k.tap_key(X.MUTE)
    elif signal == keys.RED:
        k.tap_key(X.SHUTDOWN)
    elif signal == keys.CH_UP:
        k.tap_key(X.NEXT_SONG)
    elif signal == keys.CH_DOWN:
        k.tap_key(X.PREVIOUS_SONG)
    elif signal == keys.CONFIRM:
        k.tap_key(X.PLAY_PAUSE)
    elif signal == keys.IBUTTON:
        k.tap_key(X.WWW)
    elif signal == keys.MATRIX:
        k.tap_key(X.MAIL)
    elif signal == keys.YELLOW:
        k.tap_key(X.REBOOT_SESSION)
    else:
        print("Nothing to do.")


def main():
    "Main procedure of this fucking program"
    port = list_ports()[0]
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
