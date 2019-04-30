#!/usr/bin/env python
import curses
import logging

from geojsonwatcher.fetch import fetch_data
from geojsonwatcher.display import Display

logging.basicConfig(filename='main.log', level=logging.DEBUG)
logging.info('Application started.')

scr = curses.initscr()
display = Display(scr)
latest_report = None
running_report = None

try:
    while True:
        latest_report = display.loadingData(fetch_data)
        logging.info('latest_report : ' + str(latest_report))
        display.show_report(latest_report)
        curses.napms(60000)
except Exception as e:
    logging.error("Exception in main loop")
    logging.error(str(e))
    print(e)
finally:
    curses.endwin()
