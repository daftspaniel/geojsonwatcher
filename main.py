#!/usr/bin/env python
import curses
import logging

from geojsonwatcher.fetch import fetch_data
from geojsonwatcher.display import Display
from geojsonwatcher.report import Report
from geojsonwatcher.common.log import setup_logging, log

setup_logging()
scr = curses.initscr()
display = Display(scr)
fetched_report = None
latest_report = None
running_report = Report('Running', {})
log('GeoJSON starting...')

try:
    while True:
        fetched_report = display.loading_data(fetch_data)
        if not fetched_report is None:
            latest_report = fetched_report
            running_report.append(latest_report)

        log('Showing latest feed report.')
        display.show_report(latest_report)
        curses.napms(30000)
        log('Showing runnning report.')
        display.show_report(running_report)
        curses.napms(30000)
except Exception as e:
    logging.error("Exception in main loop")
    logging.error(str(e))
finally:
    curses.endwin()
