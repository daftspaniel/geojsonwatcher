#!/usr/bin/env python
import logging
import time

from geojsonwatcher.fetch import fetch_data
from geojsonwatcher.display import Display
from geojsonwatcher.data_structures.report import Report
from geojsonwatcher.common.log import setup_logging, log
from geojsonwatcher.storage.feature_store import FeatureStore

setup_logging()
display = Display()
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
        time.sleep(30)
        
        log('Showing runnning report.')
        display.show_report(running_report)
        time.sleep(30)
except Exception as e:
    print(str(e))
    logging.error("Exception in main loop")
    logging.error(str(e))
