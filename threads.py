import threading
import time
from Adafruit_LED_Backpack import SevenSegment


alarms = []
comm = None
display = None
colon = False


def init_display():
    global display

    display = SevenSegment.SevenSegment()
    display.begin()


def runner(c):
    global comm
    
    comm = c


def clock():
    global display, colon

    if display is None:
        init_display()

    display.clear()
    display.print_number_str(time.strftime('%I%M'))
    display.set_colon(colon)
    display.write_display()

    colon = not colon