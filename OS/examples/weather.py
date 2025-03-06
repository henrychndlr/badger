import badger2040
from badger2040 import WIDTH
import urequests
import pngdec


# Display Setup
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(2)

png = pngdec.PNG(display.display)

temperature = 3.5
windspeed = 0.5
winddirection = "NW"
weathercode = 0
date, time = "2025-03-04", "21:30"

def draw_page():
    # Clear the display
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    # Draw the page header
    display.set_font("bitmap6")
    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 20)
    display.set_pen(15)
    display.text("Weather", 3, 4)
    display.set_pen(0)

    display.set_font("bitmap8")

    if temperature is not None:
        # Choose an appropriate icon based on the weather code
        # Weather codes from https://open-meteo.com/en/docs
        # Weather icons from https://fontawesome.com/
        if weathercode in [71, 73, 75, 77, 85, 86]:  # codes for snow
            png.open_file("/icons/icon-snow.png")
        elif weathercode in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:  # codes for rain
            png.open_file("/icons/icon-rain.png")
        elif weathercode in [1, 2, 3, 45, 48]:  # codes for cloud
            png.open_file("/icons/icon-cloud.png")
        elif weathercode in [0]:  # codes for sun
            png.open_file("/icons/icon-sun.png")
        elif weathercode in [95, 96, 99]:  # codes for storm
            png.open_file("/icons/icon-storm.png")
        png.decode(13, 40)
        display.set_pen(0)
        display.text(f"Temperature: {temperature}°C", int(WIDTH / 3), 28, WIDTH - 105, 2)
        display.text(f"Wind Speed: {windspeed}kmph", int(WIDTH / 3), 48, WIDTH - 105, 2)
        display.text(f"Wind Direction: {winddirection}", int(WIDTH / 3), 68, WIDTH - 105, 2)
        display.text(f"Last update: {date}, {time}", int(WIDTH / 3), 88, WIDTH - 105, 2)

    else:
        display.set_pen(0)
        display.rectangle(0, 60, WIDTH, 25)
        display.set_pen(15)
        display.text("Unable to display weather! Check your network settings in WIFI_CONFIG.py", 5, 65, WIDTH, 1)

    display.update()


draw_page()

# Call halt in a loop, on battery this switches off power.
# On USB, the app will exit when A+C is pressed because the launcher picks that up.
while True:
    display.keepalive()
    display.halt()