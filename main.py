from microbit import *

# constants
Motor = {"Left": 8448, "Right": 8192}       # motor i2c addresses
MotorPower = {"On": 28673, "Off": 28672}    #

if __name__ == "__main__":
    display.scroll('Hello, World!')
    display.show(Image.HEART_SMALL)
    sleep(5000)