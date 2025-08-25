from datetime import datetime, timezone
def to_epoch_millis(date_str: str) -> int:
    """
    Convert 'YYYY-MM-DD HH:MM' in local time to epoch ms in UTC
    """
    # Parse string as local time
    local_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

    # Convert to UTC
    utc_dt = local_dt.astimezone(timezone.utc)

    # Return milliseconds
    return int(utc_dt.timestamp() * 1000)

