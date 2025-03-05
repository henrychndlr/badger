import badger2040
from badger2040 import WIDTH
import pngdec
import time
import machine
import rc522

TEXT_SIZE = 1
LINE_HEIGHT = 15
tagUID = "4D:05:4F:71"  # The UID you want to emulate
tagType = "ISO 14443-3A"  # Type of the RFID tag (ISO 14443-3A in this case)

# Set up the display
display = badger2040.Badger2040()
display.led(128)
png = pngdec.PNG(display.display)

# Clear to white
display.set_pen(15)
display.clear()

# Display the BadgerOS info
display.set_font("bitmap8")
display.set_pen(0)
display.rectangle(0, 0, WIDTH, 16)
display.set_pen(15)
display.text("badgerOS", 3, 4, WIDTH, 1)
display.text("RFID", WIDTH - display.measure_text("help", 0.4) - 4, 4, WIDTH, 1)

# Initialize RC522 reader
spi = machine.SPI(1, baudrate=5000000, polarity=0, phase=0)  # SPI interface
rc522_reader = rc522.RC522(spi, machine.Pin(5), machine.Pin(4))  # SDA (5) and RST (4) pins

# Set font and text color for UID and tag info
display.set_pen(0)
display.set_font("bitmap14_outline")

def read_rfid():
    display.text("Waiting for tag...", 0, 30, WIDTH, TEXT_SIZE)
    display.update()

    # Loop to detect a tag
    while True:
        uid = rc522_reader.read_uid()
        if uid:
            uid_hex = ":".join(["{:02X}".format(x) for x in uid])
            display.set_pen(15)
            display.clear()  # Clear screen before displaying the UID
            display.set_pen(0)
            display.text(f"Tag detected!", 0, 30, WIDTH, TEXT_SIZE)
            display.text(f"UID: {uid_hex}", 0, 45, WIDTH, TEXT_SIZE)
            display.text(f"Emulating UID: {tagUID}", 0, 60, WIDTH, TEXT_SIZE)
            display.update()
            time.sleep(1)  # Wait a bit before continuing to check for tags

# Emulate the RFID tag with the specified UID
read_rfid()

# Keep the display on and handle power management
while True:
    display.keepalive()
    display.halt()
