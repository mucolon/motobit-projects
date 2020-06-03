# This file commands the the micro:bot to follow a 2 inch wide black line.
# The MotoBit class is included, thus this is the only file that needs to be flashed.

from microbit import display, Image, i2c, pin0, pin1, pin2, sleep


class MotoBit():
    '''Initialize moto:bit hardware.
    Args:
        invert_left (bool): Invert left motor polarity. (default: False)
        invert_right (bool): Invert right motor polarity. (default: False)
        line_threshold (int): Threshold value for detecting a dark line. Run ir_read.py to read values on REPL.
            [0, 1023] (default: 850)
    '''
    I2C_ADDR = 0x59         # 89
    CMD_ENABLE = 0x70       # 112
    CMD_SPEED_LEFT = 0x21   # 33
    CMD_SPEED_RIGHT = 0x20  # 32
    DUTY_NEG_CTE = 0x7f     # 127
    DUTY_POS_CTE = 0x80     # 128
    DUTY_MAX = 0xff         # 255

    def __init__(self, invert_left=False, invert_right=False, line_threshold=850):
        self.INVERT = (invert_left, invert_right)
        self.threshold = line_threshold

    def enable(self):
        '''Enable motor driver.
        '''
        i2c.write(self.I2C_ADDR, bytes([self.CMD_ENABLE, 0x01]))

    def disable(self):
        '''Disable motor driver.
        '''
        i2c.write(self.I2C_ADDR, bytes([self.CMD_ENABLE, 0x00]))

    def drive(self, speed_left, speed_right):
        '''Drive motors continuously based on 100 point scale.
        Args:
            speed_left (int|float): Motor power value. [-100, 100]
            speed_right (int|float): Motor power value. [-100, 100]
        '''
        speeds = [speed_left, speed_right]
        for i in range(2):
            if self.INVERT[i]:
                speeds[i] = -speeds[i]
            if speeds[i] <= 0:
                if speeds[i] < -100:
                    speeds[i] = -100
                speeds[i] = round(speeds[i] * 127 / 100) + self.DUTY_NEG_CTE
            elif speeds[i] > 0:
                if speeds[i] > 100:
                    speeds[i] = 100
                speeds[i] = round(speeds[i] * 127 / 100) + self.DUTY_POS_CTE
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_LEFT, speeds[0]]))
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_RIGHT, speeds[1]]))

    def drive_stop(self, speed_left, speed_right, duration):
        '''Drive motors for time duration based on 100 point scale.
        Args:
            speed_left (int|float): Motor power value. [-100, 100]
            speed_right (int|float): Motor power value. [-100, 100]
            duration (int): Time the motors will run in milliseconds. [1, infinity)
        '''
        self.drive(speed_left, speed_right)
        sleep(duration)
        self.drive(0, 0)

    def ir_left(self):
        '''Returns True if left sensor is above a dark line.
        '''
        return pin0.read_analog() >= self.threshold

    def ir_center(self):
        '''Returns True if center sensor is above a dark line.
        '''
        return pin1.read_analog() >= self.threshold

    def ir_right(self):
        '''Returns True if right sensor is above a dark line.
        '''
        return pin2.read_analog() >= self.threshold


speed = 20
speed_diff = 10
mod = 1
gain = 0.5
time = 450
moto = MotoBit(invert_right=True)
moto.enable()
while True:
    # reading analog values
    sensor_left = moto.ir_left()
    sensor_center = moto.ir_center()
    sensor_right = moto.ir_right()
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
