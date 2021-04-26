#!/usr/bin/env python
import curses
import logging

from geojsonwatcher.common.log import setup_logging, log
from geojsonwatcher.data_structures.report import Report
from geojsonwatcher.display import Display
from geojsonwatcher.fetch import fetch_data
from geojsonwatcher.storage.feature_store import FeatureStore
from geojsonwatcher.storage.store_management import get_feature_store_path

DELAY = 30000


def main():
    setup_logging()

    scr = curses.initscr()
    display = Display(scr)

    storage = FeatureStore(get_feature_store_path())
    storage.connect()
    latest_report = None
    running_report = Report('Running', {})
    log('GeoJSON starting...')

    try:
        while True:
            fetched_report = display.loading_data(fetch_data)
            if fetched_report is not None:
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
            curses.napms(DELAY)
            if display.check_for_resize():
                log('Resize')
                display.draw_core_screen()

            log('Showing running report.')
            display.show_report(running_report)
            curses.napms(DELAY)
    except Exception as e:
        logging.error("Exception in main loop")
        logging.error(str(e))
        print("Exception in main loop")
        print(str(e))
    finally:
        curses.endwin()
