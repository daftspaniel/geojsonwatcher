#!/usr/bin/env python
import curses
import logging

from geojsonwatcher.fetch import fetch_data
from geojsonwatcher.display import Display
from geojsonwatcher.data_structures.report import Report
from geojsonwatcher.common.log import setup_logging, log
from geojsonwatcher.storage.feature_store import FeatureStore

setup_logging()
scr = curses.initscr()
display = Display(scr)
storage = FeatureStore('quakes.db')
storage.connect()
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
        
            log('Storing report.')
            storage.connect()
            for entry in latest_report.entries:
                storage.store_feature(entry)
            storage.connection.commit()
            storage.disconnect()

        log('Showing latest feed report.')
        display.show_report(latest_report)
        curses.napms(30000)
        if display.check_for_resize():
            log('Something went wrong')
        
        log('Showing runnning report.')
        display.show_report(running_report)
        curses.napms(30000)
except Exception as e:
    logging.error("Exception in main loop")
    logging.error(str(e))
finally:
    curses.endwin()
