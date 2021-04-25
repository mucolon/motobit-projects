from microbit import sleep, display, Image, pin0, pin1


def encoders(threshold=150):
    left = pin0.read_analog()
    right = pin1.read_analog()
    l, r = 1, 1
    count_l, count_r = 0, 0
    if left < threshold:
        l = 0
        count_l += 1
    elif left > threshold:
        l = 1
    if right < threshold:
        r = 0
        count_r += 1
    elif right > threshold:
        r = 1
    return (l, r, count_l, count_r)


display.show(Image.NO, clear=True, delay=1500)

while True:
    data = encoders()
    print((data[2], data[3]))
