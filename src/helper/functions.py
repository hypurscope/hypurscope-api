from src.validator.defi import Protocol
import httpx
from src.helper.db import get_client
from datetime import datetime, timezone
from src.config import defi_url


async def process_defi():
    async with httpx.AsyncClient() as client:
        value = await client.get(defi_url)
    protocol = Protocol.model_validate(value.json())
    return protocol


async def get_defi_from_db():
    client = get_client()
    database = client["defi-db"]
    collection = database["defi"]
    query_filter = {
        "name": "Hyperliquid",
    }
    data = collection.find_one(query_filter)
    return data


async def save_or_update_defi_to_db(updated_data: Protocol):
    client = get_client()
    database = client["defi-db"]
    collection = database["defi"]
    query_filter = {
        "name": "Hyperliquid",
    }
    data = collection.find_one(query_filter)
    replace_doc = updated_data.model_dump()
    if data:
        collection.replace_one(query_filter, replace_doc)
    else:
        collection.insert_one(replace_doc)


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
