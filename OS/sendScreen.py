import badger2040
import sys
import time

badger = badger2040.Badger2040()

while True:
    cmd = sys.stdin.readline().strip()  # Read command from USB
    if cmd == "CAPTURE":
        sys.stdout.buffer.write(badger.image())  # Send screen data
        sys.stdout.flush()
    time.sleep(0.1)
