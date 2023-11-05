import serial
import time

ghost = False

arduino = serial.Serial(port='/dev/ttyACM0',  baudrate=9600, timeout=.1)

def init():
    time.sleep(5)
    arduino.write("home".encode())
    time.sleep(5)
    print("furby init")

def sleep():
    arduino.write("home".encode())
    time.sleep(5)
    arduino.write("sleep".encode())
    time.sleep(5)
    print("furby sleep")

def wake():
    arduino.write("wake".encode())
    time.sleep(5)
    arduino.write("home".encode())
    time.sleep(5)
    print("furby wake")

def boogie():
    arduino.write("home".encode())
    time.sleep(5)
    arduino.write("sleep".encode())
    time.sleep(5)
    print("furby boogie")

def freeze():
    arduino.write("home".encode())
    time.sleep(5)
    print("furby stop boogie")

def reset():
    arduino.write("home".encode())
    time.sleep(5)
    print("furby reset")
