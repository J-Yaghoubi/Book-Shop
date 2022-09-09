import os
import logging


def clear_screen():
    os.system('clear') if os.name == 'posix' else os.system('cls')


def run_logger():
    fm = "%(asctime)s - (%(name)-20s) - %(levelname)-12s: %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=fm, filename='logs/log.txt', \
                                                filemode='a', encoding='utf-8')
    
    logger = logging.getLogger(__name__)                                            
    logger.info('Program has been started...')
   