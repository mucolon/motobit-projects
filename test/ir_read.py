from microbit import *

while True:
    if button_a.was_pressed():
        while True:
            sensor_left = pin0.read_analog()
            sensor_center = pin1.read_analog()
            sensor_right = pin2.read_analog()
            print((sensor_left, sensor_center, sensor_right))
            sleep(10)
            display.show(Image.NO, clear=True)
            if button_b.was_pressed():
                break
        break
    else:
        display.show(Image.ARROW_W, clear=True)
        sleep(100)

display.show(Image.YES)
