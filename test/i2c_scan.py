from microbit import *

i2c.init()
addresses = i2c.scan()

for address in addresses:
    display.scroll(address)
    sleep(1000)