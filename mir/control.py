#!/usr/bin/python
# coding=utf-8


# third-library
import serial
from serial.tools.list_ports import comports as list_ports
import pykeyboard
import pymouse

# self-package
import mir.keys

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


def main():
    "Main procedure of this fucking program"
    port = list_ports()[0]
    conn = connect(port.device)
    stream = stream_connection(conn)
    for signal in stream:
        interpreter(signal)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutdown. Bye!")
