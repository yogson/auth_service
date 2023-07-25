from datetime import datetime


def get_utcnow_timestamp():
    return int(datetime.utcnow().timestamp())