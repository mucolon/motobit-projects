from microbit import i2c, display, sleep

i2c.init()
addresses = i2c.scan()

for address in addresses:
    display.scroll(address)
    sleep(500)
