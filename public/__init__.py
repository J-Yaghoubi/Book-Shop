
import logging


# Initialize logging

fm = "%(asctime)s (%(name)s) %(levelname)-12s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=fm, filename='logs/log.txt', \
                                            filemode='a', encoding='utf-8')


logging.info('Program has been started')