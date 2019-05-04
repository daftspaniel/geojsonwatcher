import logging

logger = None


def setup_logging():
    logging.basicConfig(
        filename='log.txt',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

def log(text):
    logging.info(text)
