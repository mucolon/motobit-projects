from microbit import sleep, display, Image, pin0, pin1, pin2

while True:
    sensor_left = pin0.read_analog()
    sensor_center = pin1.read_analog()
    sensor_right = pin2.read_analog()
    print((sensor_left, sensor_center, sensor_right))
    sleep(10)
    display.show(Image.NO, clear=True)
