from microbit import *
import ustruct

class MotoBit:
    motor_left = 8448
    motor_right = 8192
    motor_on = 28673
    motor_off = 28672
    motor_forward = 0
    motor_reverse = 1
    motor_address = 89

    def __init__(self):
        i2c.init()

    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        return ((value - fromLow) * (toHigh - toLow)) / (fromHigh - fromLow) + toLow

    def i2c_write(self, address, value):
        buf = ustruct.pack(">4i", value)
        # i2c.write(address << 1, buf)
        i2c.write(address, buf)

    def setMotorSpeed(self, motor, direction, speed):
        speed = abs(speed)
        if speed > 100:
            speed = 100
        if direction == self.motor_forward:
            pwr = self.map(speed, 0, 100, 0, 127)
            pwr = round(pwr)
            pwr = 128 + pwr
            if pwr > 255:
                pwr = 255
        else:
            pwr = self.map(speed, 0, 100, 127, 0)
            pwr = round(pwr)
        i2c_write(self.motor_address, (motor + pwr))

    def enable(self, motor_power):
        i2c_write(self.motor_address, motor_power)

    def invert(self, motor, invert):
        temp_num = 1 if invert else 0
        if motor == self.motor_right:
            i2c_write(self.motor_address, (4608 + temp_num))
        else:
            i2c_write(self.motor_address, (4864 + temp_num))


if __name__ == "__main__":

    moto = MotoBit()
    moto.invert(moto.motor_left, True)
    moto.invert(moto.motor_right, False)
    moto.enable(moto.motor_on)
    moto.setMotorSpeed(moto.motor_left, moto.motor_forward, 25)
    moto.setMotorSpeed(moto.motor_right, moto.motor_forward, 25)
    sleep(1000 * 15)
    moto.enable(moto.motor_off)
