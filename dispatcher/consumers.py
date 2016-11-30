import time
import logging
import uuid

from channels.channel import Channel

logger = logging.getLogger('django')


def submit_mission(message):
    uid = uuid.uuid4()
    logger.info('send uuid %s' % uid.hex)
    Channel('counter').send({'uuid': uid.hex})


def counter(message):
    logger.info('get uuid %s' % message['uuid'])
    for i in range(5):
        logger.info('counter %s count %d' % (message['uuid'], i))
    message.reply_channel.send(message['uuid'])
