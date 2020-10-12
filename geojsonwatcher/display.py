import datetime
import logging

from geojsonwatcher.common.log import log
from geojsonwatcher.common.util import get_time, timestamp_to_string
from geojsonwatcher.data_structures.report import Report

"""
    Display app in a Curses window.
"""


class Display(object):
    def __init__(self):
        # Draw core screen.
        print("GJWatcher v0.1te")

    def enter_loading_state(self):
        print("Connecting...")

    def exit_loading_state(self):
        print("Connected.")

    def show_report(self, report: Report):
        if report is None:
            return
        print(report.name.ljust(10))

        if report is None:
            print('Could not read feed')
            return
        logging.info('show report :: ' + str(report.name))
        print(str(datetime.datetime.now().time()))
        print(timestamp_to_string(
            report.metadata['generated']))
        print(str(len(report.entries)).ljust(5))
        print(str(report.updates).ljust(5))
        line = 3
        for entry in report.entries:
            print(entry.mag + " " + entry.time +
                  " " + entry.site + " " + entry.area)
            line += 1
        logging.info('Report complete.')

    def show_error(self, e):
        # print(self.error_text[0])
        # print(self.error_text[1])
        print("Error updating at " + get_time())

    def loading_data(self, fetch_method):
        report = None
        try:
            self.enter_loading_state()
            report = fetch_method()
            logging.info('latest_report :: ' + str(report))
            self.exit_loading_state()
        except Exception as e:
            logging.error("Exception in loading_data")
            logging.error(str(e))
            print('Loading data error!')
        logging.info('Returning : ' + str(report) + '.')
        return report
