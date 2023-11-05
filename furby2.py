import serial
import time

ghost = False


def init():
    if !ghost:
        arduino = serial.Serial(port='/dev/ttyACM0',  baudrate=115200, timeout=.1)
        time.sleep(5)
        arduino.write("home".encode())
        time.sleep(5)
    print("furby init")

def sleep():
    if !ghost:
        arduino.write("home".encode())
        time.sleep(5)
        arduino.write("sleep".encode())
        time.sleep(5)
    print("furby sleep")

def wake():
    if !ghost:
        arduino.write("wake".encode())
        time.sleep(5)
        arduino.write("home".encode())
        time.sleep(5)
    print("furby wake")

def boogie():
    if !ghost:
        arduino.write("home".encode())
        time.sleep(5)
        arduino.write("sleep".encode())
        time.sleep(5)
    print("furby boogie")

def freeze():
    if !ghost:
        arduino.write("home".encode())
        time.sleep(5)
    print("furby stop boogie")

def reset():
    if !ghost:
        arduino.write("home".encode())
        time.sleep(5)
    print("furby reset")

def ghost():
    ghost = True
    print("FURBY GHOST MODE: TO PREVENT CRASHES WHEN NOT PLUGGED INTO THE FURBY")
