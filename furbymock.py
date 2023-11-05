import serial
import time

def init():
    time.sleep(10)
    print("MOCK furby init")

def sleep():
    time.sleep(10)
    print("mock furby sleep")

def wake():
    time.sleep(10)
    print("mock furby wake")

def boogie():
    time.sleep(10)
    print("mock furby boogie")

def freeze():
    time.sleep(5)
    print("mock furby stop boogie")

def reset():
    time.sleep(5)
    print("mock furby reset")
