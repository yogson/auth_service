from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def get_utcnow_timestamp():
    return int(datetime.utcnow().timestamp())