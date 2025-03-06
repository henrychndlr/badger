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
    display.text("RC522 FOUND!", 132, 40, WIDTH, TEXT_SIZE)
    display.text("EMULATING TAG...", 132, 55, WIDTH, TEXT_SIZE)
    display.text(f"UID: {tagUID}", 132, 70, WIDTH, TEXT_SIZE)
    if not tagType:
        display.text(f"TAG TYPE: ISO 14443-3A", 132, 85, WIDTH, TEXT_SIZE)
    png.open_file("/icons/rfid-symbol.png")
    png.decode(0, 10)
    
    #while True:
     #display.led(255)
        #time.sleep(1)
        #display.led(0)
        #time.sleep(1)

emulate_rfid()
display.update()

# Call halt in a loop, on battery this switches off power.
# On USB, the app will exit when A+C is pressed because the launcher picks that up.
while True:
    display.keepalive()
    display.halt()