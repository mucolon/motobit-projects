from microbit import *

i2c.init()
addresses = i2c.scan()
length = len(addresses)

for address in addresses:
    display.scroll(address)
    sleep(1000)