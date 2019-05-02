import curses
import datetime
import logging

from geojsonwatcher.util import *
from geojsonwatcher.util import getTime


class Display(object):
    def __init__(self, scr):
        self.scr = scr
        self.scr.border()
        self.scr.addstr(1, 64, "GJWatcher v0.1", curses.A_UNDERLINE)
        self.scr.addstr(21, 2, "Loaded    : ",  curses.A_REVERSE)
        self.scr.addstr(20, 2, "Timestamp : ",  curses.A_REVERSE)
        self.scr.refresh()

    def clearDisplay(self):
        for l in range(14):
            self.scr.addstr(l + 3, 2, ''.ljust(70))
        self.scr.addstr(20, 14, ''.ljust(50))
        self.scr.addstr(21, 14, ''.ljust(50))

    def enter_loading_state(self):
        self.scr.addstr(2, 2, "Connecting...", curses.A_BLINK)
        self.scr.refresh()

    def exit_loading_state(self):
        self.scr.addstr(2, 2, "                 ")
        self.scr.refresh()

    def show_report(self, report):
        self.clearDisplay()
        if report is None:
            self.scr.addstr(3, 2, 'Could not read feed')
            return 
        logging.info('show report :: ' + str(report))
        self.scr.addstr(21, 15, str(
            datetime.datetime.now().time()),  curses.A_DIM)
        self.scr.addstr(20, 15, timestamp_to_string(
            report[0]['generated']),  curses.A_DIM)
        line = 3
        for entry in report[1]:
            self.scr.addstr(line, 2, entry.mag)
            self.scr.addstr(line, 8, entry.time)
            self.scr.addstr(line, 18, entry.site)
            self.scr.addstr(line, 55, entry.area)
            line += 1
        self.scr.refresh()
        logging.info('Report complete.')

    def show_error(self, e):
        self.scr.addstr(21, 21, "Error updating at " +
                        getTime(), curses.A_BLINK)

    def loadingData(self, fetchMethod):
        report = None
        try:
            self.enter_loading_state()
            report = fetchMethod()
            logging.info('latest_report :: ' + str(report))
            self.exit_loading_state()
        except Exception as e:
            logging.error("Exception in loadingData")
            self.show_error(e)
        self.scr.refresh()
        logging.info('Returning : ' + str(report))
        return report
