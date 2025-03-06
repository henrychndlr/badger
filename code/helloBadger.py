import badger2040
import time
badger = badger2040.Badger2040()

badger.set_pen(15)
badger.clear()

badger.set_pen(0)
badger.set_font("sans")
badger.set_thickness(2)
badger.text("Hello Badger", 20, 40, scale=1)
badger.line(100, 90, 100, 65)
badger.line(110, 90, 110, 65)
badger.line(85, 100, 100, 110)
badger.line(100, 110, 110, 110)
badger.line(110, 110, 125, 100)
badger.update()

while True:
    badger.led(255)
    time.sleep(0.5)
    badger.led(0)
    time.sleep(0.5)
