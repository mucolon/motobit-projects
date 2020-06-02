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


speed = 20
speed_diff = 10
mod = 1
gain = 0.5
time = 500
moto = MotoBit(invert_right=True, line_threshold=850)
moto.enable()
while True:
    sensor_left = moto.ir_left()
    sensor_center = moto.ir_center()
    sensor_right = moto.ir_right()
    if (sensor_left & sensor_center & sensor_right):
        display.show(Image.ARROW_N, clear=True)                 # straight
        moto.drive_stop(speed, speed, time)
        mod = 1
    elif ((not sensor_left) & sensor_center & sensor_right):
        display.show(Image.ARROW_NE, clear=True)                # turn right
        moto.drive_stop(speed + speed_diff, speed, time)
        mod = 1
    elif (sensor_left & sensor_center & (not sensor_right)):
        display.show(Image.ARROW_NW, clear=True)                # turn left
        moto.drive_stop(speed, speed + speed_diff, time)
        mod = 1
    elif ((not sensor_left) & (not sensor_center) & sensor_right):
        display.show(Image.ARROW_S, clear=True)                 # reverse
        moto.drive_stop(-speed, -speed, time)
        sleep(10)
        display.show(Image.ARROW_NE, clear=True)                # turn right
        moto.drive_stop(speed + (speed_diff * mod), speed, time)
        mod += gain
    elif (sensor_left & (not sensor_center) & (not sensor_right)):
        display.show(Image.ARROW_S, clear=True)                 # reverse
        moto.drive_stop(-speed, -speed, time)
        sleep(10)
        display.show(Image.ARROW_NW, clear=True)                # turn left
        moto.drive_stop(speed, speed + (speed_diff * mod), time)
        mod += gain
    else:
        display.show(Image.ARROW_S, clear=True)                 # reverse
        moto.drive_stop(-speed, -speed, time)
        mod = 1
