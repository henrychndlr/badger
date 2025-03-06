import badger2040
from badger2040 import WIDTH
import pngdec
import time

TEXT_SIZE = 1
LINE_HEIGHT = 15
tagUID = "4D:05:4F:71"
tagType = ""

display = badger2040.Badger2040()
display.led(128)
png = pngdec.PNG(display.display)

# Clear to white
display.set_pen(15)
display.clear()

display.set_font("bitmap8")
display.set_pen(0)
display.rectangle(0, 0, WIDTH, 16)
display.set_pen(15)
display.text("badgerOS", 3, 4, WIDTH, 1)
display.text("RFID", WIDTH - display.measure_text("help", 0.4) - 4, 4, WIDTH, 1)

display.set_pen(0)
display.set_font("bitmap14_outline")

def emulate_rfid():
    display.text("RC522 Found!", 0, 30, WIDTH, TEXT_SIZE)
    display.text("EMULATING TAG...", 0, 45, WIDTH, TEXT_SIZE)
    display.text(f"UID: {tagUID}", 0, 60, WIDTH, TEXT_SIZE)
    if not tagType:
        display.text(f"Tag Type: ISO 14443-3A", 0, 75, WIDTH, TEXT_SIZE)
    png.open_file("/icons/rfid-symbol.png")
    png.decode(168, 10)
    
    while True:
        display.led(255)
        time.sleep(1)
        display.led(0)
        time.sleep(1)

emulate_rfid()
display.update()

# Call halt in a loop, on battery this switches off power.
# On USB, the app will exit when A+C is pressed because the launcher picks that up.
while True:
    display.keepalive()
    display.halt()

