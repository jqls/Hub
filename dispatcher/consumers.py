import time
import logging

logger = logging.getLogger('django')


def submit_mission(message):
    for i in range(10):
        logger.info('submit mission %d', i)
        time.sleep(1)
