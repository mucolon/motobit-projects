from microbit import *


def test_duty():
    # testing drive_duty method
    duty = 0
    moto = MotoBit(invert_right=True)
    moto.enable()
    while duty <= moto.DUTY_MAX:
        display.show(duty)
        moto.drive_duty(duty, duty)
        duty += 1
    moto.disable()


def test_drive():
    # testing drive method
    speed = -100
    moto = MotoBit(invert_right=True)
    moto.enable()
    while speed <= 100:
        display.show(speed)
        moto.drive(speed, speed)
        speed += 10
        sleep(100)
    moto.disable()


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


class MotoBit():
    '''Initialize moto:bit hardware.
    Args:
        invert_left (bool): Invert left motor polarity. (default: False)
        invert_right (bool): Invert right motor polarity. (default: False)
        black_threshold (int): Threshold value for detecting a black line. Run ir_read.py to read values on REPL.
            [0, 1023] (default: 825)
    '''
    I2C_ADDR = 0x59         # 89
    CMD_ENABLE = 0x70       # 112
    CMD_SPEED_LEFT = 0x21   # 33
    CMD_SPEED_RIGHT = 0x20  # 32
    DUTY_MIN = 0x00         # 0
    DUTY_NEG_CTE = 0x7f     # 127
    DUTY_POS_CTE = 0x80     # 128
    DUTY_MAX = 0xff         # 255

    def __init__(self, invert_left=False, invert_right=False, black_threshold=825):
        self.invert_left = invert_left
        self.invert_right = invert_right
        self.INVERT = (invert_left, invert_right)
        self.threshold = black_threshold

    def enable(self):
        '''Enable motor driver.
        '''
        i2c.write(self.I2C_ADDR, bytes([self.CMD_ENABLE, 0x01]))

    def disable(self):
        '''Disable motor driver.
        '''
        i2c.write(self.I2C_ADDR, bytes([self.CMD_ENABLE, 0x00]))

    def drive(self, speed_left, speed_right):
        '''Drive motors based on 100 point scale.
        Args:
            speed_left (int|float): Motor power value. [-100, 100]
            speed_right (int|float): Motor power value. [-100, 100]
        '''
        speeds = [speed_left, speed_right]
        for i in range(len(speeds)):
            # if self.INVERT[i] == True:
            if self.INVERT[i]:
                speeds[i] = -1 * speeds[i]
            if speeds[i] < 0:
                if speeds[i] < -100:
                    speeds[i] = -100
                speeds[i] = round(speeds[i] * 127 / 100) + self.DUTY_NEG_CTE
            elif speeds[i] >= 0:
                if speeds[i] > 100:
                    speeds[i] = 100
                speeds[i] = round(speeds[i] * 127 / 100) + self.DUTY_POS_CTE
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_LEFT, speeds[0]]))
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_RIGHT, speeds[1]]))

    def drive_duty(self, speed_left, speed_right):
        '''Drive motors based on duty cycle values.
        Args:
            speed_left (int): Duty cycle value. [0, 255]
            speed_right (int): Duty cycle value. [0, 255]
        '''
        speeds = [speed_left, speed_right]
        for i in range(len(speeds)):
            # if self.INVERT[i] == True:
            if self.INVERT[i]:
                speeds[i] = self.DUTY_MAX - speeds[i]
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_LEFT, speeds[0]]))
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_RIGHT, speeds[1]]))

    def ir_left(self):
        '''Returns True if left sensor is above a black line.
        '''
        return pin0.read_analog() >= self.threshold

    def ir_center(self):
        '''Returns True if center sensor is above a black line.
        '''
        return pin1.read_analog() >= self.threshold

    def ir_right(self):
        '''Returns True if right sensor is above a black line.
        '''
        return pin2.read_analog() >= self.threshold


while True:
    if button_a.was_pressed():
        # test_duty()
        # test_drive()
        line_track(14, 4)
        break
    else:
        display.show(Image.ARROW_W, clear=True)
        sleep(100)

display.show(Image.YES)
