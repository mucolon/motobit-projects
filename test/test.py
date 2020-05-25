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

def test_analog():
    # testing analog sensors
    while True:
        sensor_left = pin0.read_analog()
        sensor_middle = pin1.read_analog()
        sensor_right = pin2.read_analog()
        print((sensor_left, sensor_middle, sensor_right))
        sleep(10)
        display.show(Image.NO, clear=True)
        if button_b.was_pressed():
            break

def line_track(default_speed):
    # line tracking function
    ELEC_TAPE_THRESHOLD = 850
    count_left = 0
    count_middle = 0
    count_right = 0
    moto = MotoBit(invert_right=True)
    moto.enable()
    while True:
        sensor_left = pin0.read_analog()
        sensor_middle = pin1.read_analog()
        sensor_right = pin2.read_analog()
        if sensor_left >= ELEC_TAPE_THRESHOLD:



class MotoBit():
    '''Initialize moto:bit hardware.
    Args:
        invert_left (bool): Invert left motor polarity. (default: False)
        invert_right (bool): Invert right motor polarity. (default: False)
    '''
    I2C_ADDR = 0x59         # 89
    CMD_ENABLE = 0x70       # 112
    CMD_SPEED_LEFT = 0x21   # 33
    CMD_SPEED_RIGHT = 0x20  # 32
    DUTY_MIN = 0x00         # 0
    DUTY_NEG_CTE = 0x7f     # 127
    DUTY_POS_CTE = 0x80     # 128
    DUTY_MAX = 0xff         # 255

    def __init__(self, invert_left=False, invert_right=False):
        self.invert_left = invert_left
        self.invert_right = invert_right
        self.INVERT = (invert_left, invert_right)

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
            speed_left (int|float): motor power value [-100, 100]
            speed_right (int|float): motor power value [-100, 100]
        '''
        speeds = [speed_left, speed_right]
        for i in range(len(speeds)):
            if self.INVERT[i] == True:
                speeds[i] = -1 * speeds[i]
            if speeds[i] < 0:
                if speeds[i] < -100:
                    speeds[i] = -100
                speeds[i] = round(speeds[i] * 127 / 100) + self.DUTY_NEG_CTE
            elif speeds[i] > 0:
                if speeds[i] > 100:
                    speeds[i] = 100
                speeds[i] = round(speeds[i] * 127 / 100) + self.DUTY_POS_CTE
            else:
                speeds[i] = self.DUTY_POS_CTE
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_LEFT, speeds[0]]))
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_RIGHT, speeds[1]]))

    def drive_duty(self, speed_left, speed_right):
        '''Drive motors based on duty cycle values.
        Args:
            speed_left (int): duty cycle value [0, 255]
            speed_right (int): duty cycle value [0, 255]
        '''
        speeds = [speed_left, speed_right]
        for i in range(len(speeds)):
            if self.INVERT[i] == True:
                speeds[i] = self.DUTY_MAX - speeds[i]
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_LEFT, speeds[0]]))
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_RIGHT, speeds[1]]))

while True:
    if button_a.was_pressed():
        # test_duty()
        # test_drive()
        test_analog()
        break
    else:
        display.show(Image.ARROW_W, clear=True)
        sleep(100)

display.show(Image.YES)
