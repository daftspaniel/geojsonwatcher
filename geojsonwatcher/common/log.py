""" Application logging setup and convenience functions. """
import os
import logging


def setup_logging():
    """ Creates log directory and configures logging feature."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(
        filename='logs/log.txt',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')


def log(text):
    """ Log out text at info level. """
    logging.info(text)
