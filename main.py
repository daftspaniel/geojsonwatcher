#!/usr/bin/env python
import curses
import datetime

from geojsonwatcher.fetch import fetch_data
from geojsonwatcher.util import *

scr = curses.initscr()
scr.keypad(0)
curses.noecho()
scr.border()
scr.addstr(1, 64, "GJWatcher v0.1", curses.A_UNDERLINE)


def fetchAndDisplay():
    scr.addstr(21, 2, "Loading")
    try:
        report = fetch_data()
        scr.addstr(21, 2, "Loaded: ",  curses.A_REVERSE)
        scr.addstr(20, 2, "Timestamp: ",  curses.A_REVERSE)
        scr.addstr(21, 15, str(datetime.datetime.now().time()),  curses.A_DIM)
        scr.addstr(20, 15, timestamp_to_string(
            report[0]['generated']),  curses.A_DIM)
        line = 2

        for entry in report[1]:
            scr.addstr(line, 2, entry.mag)
            scr.addstr(line, 8, entry.time)
            scr.addstr(line, 18, entry.place)
            line += 1
    except Exception as e:
        scr.addstr(2, 2, str(e))
        scr.addstr(21, 21, "Error updating at " +
                   str(datetime.datetime.now().time()), curses.A_BLINK)
    scr.refresh()


try:
    while True:
        fetchAndDisplay()
        curses.napms(60000)
except:
    print('Error')
finally:
    curses.endwin()
