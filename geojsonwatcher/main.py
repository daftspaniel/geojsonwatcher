#!/usr/bin/env python
import curses
import logging

from geojsonwatcher.common.log import setup_logging, log
from geojsonwatcher.data_structures.report import Report
from geojsonwatcher.display import Display
from geojsonwatcher.fetch import fetch_data
from geojsonwatcher.storage.feature_store import FeatureStore
from geojsonwatcher.storage.store_management import get_feature_store_path

DELAY = 1000


def main():
    setup_logging()

    scr = curses.initscr()
    display = Display(scr)

    storage = FeatureStore(get_feature_store_path())
    storage.connect()
    latest_report = None
    running_report = Report('Running', {})
    log('GeoJSON starting...')
    tick = 0
    report = 0

    try:
        while True:
            if tick == 0:
                fetched_report = display.loading_data(fetch_data)
                if fetched_report is not None:
                    latest_report = fetched_report
                    running_report.append(latest_report)

                    log('Storing new features.')
                    storage.connect()
                    for entry in latest_report.entries:
                        storage.store_feature(entry)
                    storage.connection.commit()
                    # log('Record Count' + str(storage.get_record_count()))
                    total_features = storage.get_record_count()
                    running_report.metadata['totalFeatures'] = total_features
                    latest_report.metadata['totalFeatures'] = total_features
                    storage.disconnect()
                log('Showing latest feed report.')
                display.show_report(latest_report)
                report = 0

            elif tick == 30:
                log('Showing running report.')
                display.show_report(running_report)
                tick = 0
                report = 1

            log('TICK' + str(tick))
            # log(display.check_for_resize())
            c = scr.getch()  # Get a keystroke
            log('c'+str(c))
            if c == 113:
                curses.endwin()
                exit(0)
            elif c == curses.KEY_RESIZE or display.check_for_resize():
                log('Resize at' + str(tick))
                display.draw_core_screen()
                if report == 0:
                    display.show_report(latest_report)
                else:
                    display.show_report(running_report)

            curses.napms(DELAY)
            tick += 1
    except Exception as e:
        logging.error("Exception in main loop")
        logging.error(str(e))
        print("Exception in main loop")
        print(str(e))
    finally:
        curses.endwin()
