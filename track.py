from microbit import *
from motobit import MotoBit


def line_track(default_speed, gain):
    '''Line tracking function.
    Sensors read high when over black & low when over white.
    Args:
        default_speed (int|float): Motor power value. [-100, 100]
        gain (int|float): Proportional gain constant for self correcting. (0, infinity)
    '''
    count_left = 0
    count_right = 0
    moto = MotoBit(invert_right=True)
    moto.enable()
    while True:
        sensor_left = moto.ir_left()
        sensor_center = moto.ir_center()
        sensor_right = moto.ir_right()
        if button_b.was_pressed():
            break
        elif sensor_center:
            count_left = 0
            count_right = 0
            delta_left = 0
            delta_right = 0
            display.show(Image.ARROW_N, clear=True)
        elif sensor_left | (count_left > 0):
            count_left += gain
            delta_left = -1 * count_left
            delta_right = count_left
            display.show(Image.ARROW_W, clear=True)
        elif sensor_right | (count_right > 0):
            count_right += gain
            delta_left = count_right
            delta_right = -1 * count_right
            display.show(Image.ARROW_E, clear=True)
        else:
            pass
        moto.drive(default_speed + delta_left,
                   default_speed + delta_right)
    moto.disable()


while True:
    if button_a.was_pressed():
        line_track(14, 4)
        break
    else:
        display.show(Image.ARROW_W, clear=True)
        sleep(100)

display.show(Image.YES)
