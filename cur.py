#!/usr/bin/env python
import curses
import datetime
from fetch import fetch_data
from util import *

scr = curses.initscr()
scr.keypad(0)
curses.noecho()
scr.border()


def fetchAndDisplay():
    scr.addstr(21, 2, "Loading")
    try:
        report = fetch_data()
        scr.addstr(21, 2, "Loaded: ",  curses.A_REVERSE)
        scr.addstr(20, 2, "Feed Timestamp: ",  curses.A_REVERSE)
        scr.addstr(21, 21, str(datetime.datetime.now().time()),  curses.A_DIM)
        scr.addstr(20, 21, timestamp_to_string(report[0]['generated']),  curses.A_DIM)
        line = 4

        for entry in report[1]:
            #scr.addstr(line, 42, str(int((entry.replace('-',''))[0])))
            #scr.adds   tr(line, 2, entry, curses.color_pair((int((entry.replace('-',''))[0]))))
            scr.addstr(line, 2, entry)
            line += 1
    except Exception as e:
        scr.addstr(2, 2, str(e))
        scr.addstr(22, 21, "Error updating at " +
                   str(datetime.datetime.now().time()), curses.A_BLINK)
    scr.refresh()


try:
    while True:
        fetchAndDisplay()
        curses.napms(60000)
except:
    print('Error')  
finally:
    curses.endwin()
