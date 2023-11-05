import serial
import time

ghost = False

arduino = serial.Serial(port='/dev/ttyACM1',  baudrate=9600, timeout=.1)

def init():
    arduino.write("home".encode())
    while str(arduino.readline().decode().rstrip()) != "home return":
        time.sleep(0.05)

def sleep():
    arduino.write("home".encode())
    while str(arduino.readline().decode().rstrip()) != "home return":
        time.sleep(0.05)
    arduino.write("sleep".encode())
    while str(arduino.readline().decode().rstrip()) != "sleep return":
        time.sleep(0.05)
    print("furby sleep")

def wake():
    arduino.write("wake".encode())
    while str(arduino.readline().decode().rstrip()) != "wake return":
        time.sleep(0.05)
    arduino.write("home".encode())
    while str(arduino.readline().decode().rstrip()) != "home return":
        time.sleep(0.05)
    print("furby wake")

def boogie():
    arduino.write("home".encode())
    while str(arduino.readline().decode().rstrip()) != "home return":
        time.sleep(0.05)
    arduino.write("boogie".encode())
    while str(arduino.readline().decode().rstrip()) != "boogie return":
        time.sleep(0.05)
    print("furby boogie")

def freeze():
    arduino.write("home".encode())
    while str(arduino.readline().decode().rstrip()) != "home return":
        time.sleep(0.05)
    print("furby stop boogie")

def reset():
    arduino.write("home".encode())
    while str(arduino.readline().decode().rstrip()) != "home return":
        time.sleep(0.05)
    print("furby reset")

def startyapping():
    arduino.write("home".encode())
    while str(arduino.readline().decode().rstrip()) != "home return":
        time.sleep(0.05)
    arduino.write("speak".encode())

def stopyapping():
    arduino.write("nospeak".encode())
    time.sleep(0.1)
    while str(arduino.readline().decode().rstrip()) != "home return":
        time.sleep(0.05)
