from microbit import sleep, display, Image, accelerometer

# x: left, right
# y: forward, backward
# z: up, down

freq = 250           # [Hz]
period = 1e3 / freq  # [ms]

while True:
    # accel_x = accelerometer.get_x()
    # accel_y = accelerometer.get_y()
    # accel_z = accelerometer.get_z()
    # print((accel_x, accel_y, accel_z))
    accel_data = accelerometer.get_values()
    print(accel_data)
    sleep(period)
    display.show(Image.NO, clear=True)
