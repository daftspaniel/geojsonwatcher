import curses
import datetime
import logging

from geojsonwatcher.common.log import log
from geojsonwatcher.common.util import get_time, timestamp_to_string
from geojsonwatcher.data_structures.report import Report

"""
    Display app in a Curses window.
"""


class Display:
    def __init__(self, scr):
        self.scr = scr
        self.starty, self.startx = self.scr.getmaxyx()
        log('Screen Size : ' + str(self.starty) + ' ' + str(self.startx))

        # Set up the key screen positions.
        self.status_x = 2
        self.status_y = 2
        self.main_columns = 76
        self.main_display_line_count = 16
        self.report_name_y = 1
        self.report_name_x = 2
        self.error_text = (21, 21)
        self.footer_y = 1234
        self.draw_core_screen()

    def draw_core_screen(self):
        self.starty, self.startx = self.scr.getmaxyx()
        self.footer_y = self.starty - 4
        self.main_display_line_count = self.starty - 7
        # Draw core screen.
        self.scr.clear()
        self.scr.border()
        self.scr.addstr(1, self.startx - 16,
                        "GJWatcher v0.2", curses.A_UNDERLINE)
        self.scr.addstr(self.footer_y + 1, 2,
                        "Loaded    : ",  curses.A_REVERSE)
        self.scr.addstr(self.footer_y, 2, "Timestamp : ",  curses.A_REVERSE)
        self.scr.addstr(self.footer_y, self.main_columns // 2,
                        "Features : ",  curses.A_REVERSE)
        self.scr.addstr(self.footer_y + 1, self.main_columns // 2,
                        "Updates  : ",  curses.A_REVERSE)
        curses.curs_set(0)
        self.scr.refresh()

    def clear_display(self):
        for l in range(self.main_display_line_count):
            self.scr.addstr(l + 3, 2, ''.ljust(70))
        self.scr.addstr(self.footer_y, 14, ''.ljust(20))
        self.scr.addstr(self.footer_y + 1, 14, ''.ljust(20))

    def enter_loading_state(self):
        self.scr.addstr(self.status_y, self.status_x,
                        "Connecting...", curses.A_BLINK)
        self.scr.refresh()

    def exit_loading_state(self):
        self.scr.addstr(self.status_y, self.status_x, "".ljust(13))
        self.scr.refresh()

    def check_for_resize(self):
        return curses.is_term_resized(self.starty, self.startx)

    def show_report(self, report: Report):
        if report is None:
            return
        self.clear_display()
        self.scr.addstr(self.report_name_y, self.report_name_x,
                        report.name.ljust(10))

        if report is None:
            self.scr.addstr(3, 2, 'Could not read feed')
            return
        logging.info('show report :: ' + str(report.name))
        self.scr.addstr(self.footer_y + 1, 15, str(
            datetime.datetime.now().time()),  curses.A_DIM)
        self.scr.addstr(self.footer_y, 15, timestamp_to_string(
            report.metadata['generated']),  curses.A_DIM)
        self.scr.addstr(self.footer_y, 55, str(
            len(report.entries)).ljust(5),  curses.A_DIM)
        self.scr.addstr(self.footer_y + 1, 55,
                        str(report.updates).ljust(5),  curses.A_DIM)
        line = 3
        for entry in report.entries[:self.main_display_line_count]:
            self.scr.addstr(line, 2, entry.mag)
            self.scr.addstr(line, 8, entry.time)
            self.scr.addstr(line, 18, entry.site)
            self.scr.addstr(line, 55, entry.area)
            if self.startx > 130:
                self.scr.addstr(line, 80, entry.url)
            line += 1
        self.scr.refresh()
        logging.info('Report complete.')

    def show_error(self, e):
        self.scr.addstr(self.error_text[0], self.error_text[1], "Error updating at " +
                        get_time(), curses.A_BLINK)

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
            self.show_error(e)
        self.scr.refresh()
        logging.info('Returning : ' + str(report) + '.')
        return report
