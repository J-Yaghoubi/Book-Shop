
import logging


# Initialize logging

fm = "%(asctime)s (%(name)s) %(levelname)-12s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=fm, filename='log.txt', \
                                            filemode='a', encoding='utf-8')


