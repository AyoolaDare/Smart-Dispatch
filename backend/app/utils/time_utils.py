from datetime import datetime

def format_timestamp(ts: datetime):
    """
    Formats a datetime object into a string.
    """
    return ts.strftime("%Y-%m-%d %H:%M:%S")
