from microbit import *
# import sys

# SparkFun moto:bit python API

# class pins:

#     def __init__(self):
#         pass

    # def map(self, value, fromLow, fromHigh, toLow, toHigh):
    #     return ((value - fromLow) * (toHigh - toLow)) / (fromHigh - fromLow) + toLow

# class MotoBit(pins):
class MotoBit:
    left = 8448
    right = 8192
    on = 28673
    off = 28672
    forward = 0
    reverse = 1

    def __init__(self):
        # self.left = 8448
        # self.right = 8192
        # self.on = 28673
        # self.off = 28672
        # self.forward = 0
        # self.reverse = 1
        pass

    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        return ((value - fromLow) * (toHigh - toLow)) / (fromHigh - fromLow) + toLow

    def setMotorSpeed(self, motor, direction, speed):
        speed = abs(speed)
        if speed > 100:
            speed = 100
        if direction == self.forward:
            pwr = self.map(speed, 0, 100, 0, 127)
            pwr = round(pwr)
            pwr = 128 + pwr
            if pwr > 255:
                pwr = 255
        else:
            pwr = self.map(speed, 0, 100, 127, 0)
            pwr = round(pwr)
        i2c.write(89, bytes(motor + pwr))
        # return pwr

    def enable(self, motor_power):
        i2c.write(89, bytes(motor_power))

    def invert(self, motor, invert):
        temp_num = 1 if invert else 0
        if motor == self.right:
            i2c.write(89, bytes(4608 + temp_num))
        else:
            i2c.write(89, bytes(4864 + temp_num))


if __name__ == "__main__":

    moto = MotoBit()
    moto.invert(moto.left, True)
    moto.invert(moto.right, False)
    moto.enable(moto.on)
    moto.setMotorSpeed(moto.left, moto.forward, 25)
    moto.setMotorSpeed(moto.right, moto.backward, 25)
    sleep(1000 * 15)
    moto.enable(moto.off)

    # while True:
        # display.scroll('Hello, World!')
        # display.show(Image.HEART_SMALL)
        # print("Loop Completed")
        # sleep(1000)

