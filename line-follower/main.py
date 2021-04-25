# This file commands the the micro:bot to follow a 2 inch wide black line.
# The MotoBit class is being imported, thus this file and motobit.py need to be flashed.

from microbit import display, Image, sleep
from motobit import MotoBit

speed = 20
speed_diff = 10
mod = 1
gain = 0.5
time = 450
moto = MotoBit(invert_right=True)
moto.enable()
while True:
    # reading analog values
    sensor_left = moto.sensors()[0]
    sensor_center = moto.sensors()[1]
    sensor_right = moto.sensors()[2]
    # all sensors over black line
    # straight
    if (sensor_left & sensor_center & sensor_right):
        display.show(Image.ARROW_N)
        moto.drive_stop(speed, speed, time)
        mod = 1
    # center & right sensors over black line
    # turn right
    elif ((not sensor_left) & sensor_center & sensor_right):
        display.show(Image.ARROW_NE)
        moto.drive_stop(speed + speed_diff, speed, time)
        mod = 1
    # left & center sensors over black line
    # turn left
    elif (sensor_left & sensor_center & (not sensor_right)):
        display.show(Image.ARROW_NW)
        moto.drive_stop(speed, speed + speed_diff, time)
        mod = 1
    # right sensor over black line
    # reverse
    # turn right
    # if this is repeated, right turn will become more aggressive
    elif ((not sensor_left) & (not sensor_center) & sensor_right):
        display.show(Image.ARROW_S)
        moto.drive_stop(-speed, -speed, time)
        sleep(10)
        display.show(Image.ARROW_NE)
        moto.drive_stop(speed + (speed_diff * mod), speed, time)
        mod += gain
    # left sensor over black line
    # reverse
    # turn left
    # if this is repeated, left turn will become more aggressive
    elif (sensor_left & (not sensor_center) & (not sensor_right)):
        display.show(Image.ARROW_S)
        moto.drive_stop(-speed, -speed, time)
        sleep(10)
        display.show(Image.ARROW_NW)
        moto.drive_stop(speed, speed + (speed_diff * mod), time)
        mod += gain
    # any other sensor readings
    # reverse
    else:
        display.show(Image.ARROW_S)
        moto.drive_stop(-speed, -speed, time)
        mod = 1
