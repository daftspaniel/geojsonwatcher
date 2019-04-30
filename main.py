#!/usr/bin/env python
import curses

from geojsonwatcher.fetch import fetch_data
from geojsonwatcher.display import Display

scr = curses.initscr()
display = Display(scr)

def fetchAndDisplay():
    try:
        display.enter_loading_state()
        report = fetch_data()
        display.exit_loading_state()

        display.show_report(report)
    except Exception as e:
        display.show_error(e)
    scr.refresh()


try:
    while True:
        fetchAndDisplay()
        curses.napms(60000)
except Exception as e:
    print(e)
finally:
    curses.endwin()
