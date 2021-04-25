from microbit import sleep, display, Image, accelerometer, compass
import math

# x: left, right
# y: forward, backward
# z: up, down

freq = 10           # [Hz]
period = 1e3 / freq  # [ms]
display.show(Image.NO, delay=1000, wait=True, clear=True)

while True:
    accel_x = accelerometer.get_x()
    accel_y = accelerometer.get_y()
    # compass.heading()
    # angle = math.degrees(math.atan2(accel_y, accel_x))
    angle = math.degrees(math.atan2(accel_x, accel_y))
    print((angle, ))
    sleep(period)
