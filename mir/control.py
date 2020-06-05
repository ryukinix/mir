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
actions_labels = {
    keys.VOL_UP: "Volume up",
    keys.VOL_DOWN: "Volume down",
    keys.MUTE: "Mute",
    keys.CH_UP: "Next song",
    keys.CH_DOWN: "Previous song",
    keys.CONFIRM: "Play/Pause",
    keys.IBUTTON: "Open rhythmbox",
    keys.GUIDE: "Open spotify",
    keys.SKY: "Toggle monitor",
    keys.REFRESH: "Xflock4",
    keys.UP: "key: Up",
    keys.DOWN: "key: Down",
    keys.LEFT: "key: Left",
    keys.RIGHT: "key: Right",
    keys.PLUS: "key: Return",
    keys.INFO: "key: Space",
    keys.MENU: "key: Shift+TAB",
    keys.MATRIX: "key: TAB",
    keys.NUM_0: "Unlock password",
    keys.RED: "Play Dragon Ball Z"
}


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


def open_program(program):
    subprocess.Popen(program, stdout=open(os.devnull, "wb"))


def interpreter(signal):
    "Given a signal 8-digit hex encoded integer, make a action"
    print("SIGNAL: {:08X}".format(signal), end='')

    if signal == keys.VOL_UP:
        k.tap_key(X.VOL_DOWN)
    elif signal == keys.VOL_DOWN:
        k.tap_key(X.VOL_UP)
    elif signal == keys.MUTE:
        k.tap_key(X.MUTE)
    elif signal == keys.CH_UP:
        # k.tap_key(X.NEXT_SONG)
        k.tap_key(">")
    elif signal == keys.CH_DOWN:
        # k.tap_key(X.PREVIOUS_SONG)
        k.tap_key("<")
    elif signal == keys.CONFIRM:
        # k.tap_key(X.PLAY_PAUSE)
        k.tap_key(" ")
    elif signal == keys.IBUTTON:
        open_program("/usr/bin/rhythmbox-client")
    elif signal == keys.GUIDE:
        open_program("spotify")
    elif signal == keys.NUM_0:
        open_program("/home/lerax/remote_unlock.sh")
    elif signal == keys.SKY:
        toggle_monitor()
    elif signal == keys.REFRESH:
        os.system('xflock4')
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
    elif signal == keys.RED:
        open_program("/home/lerax/Desktop/dragon-ball-z/play.sh")
    else:
        print(" - Ignored.")
        return
    print(" - Action made: {}".format(actions_labels.get(signal)))


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
        try:
            interpreter(signal)
        except ValueError as e:
            print('Exception ignored: ', e)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutdown. Bye!")
    except SerialException:
        print("Device unplugged. Shutdown.")
