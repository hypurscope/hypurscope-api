from fastapi import HTTPException
from src.validator.defi import Protocol
import httpx
from src.helper.db import get_client
from src.config import defi_url
from src.validator.user import TrackData
from src.helper.user_functions import all_user_data_without_fills
from collections import defaultdict

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
    client = await get_client()
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



async def save_tracking_data(data: TrackData):
    client = await get_client()
    database = client["defi-db"]
    collection = database["wallet-track"]
    query_filter = {"id": data.id, "email": data.email}
    result = collection.find_one(query_filter)
    if result:
        raise HTTPException(
            detail="Wallet already being tracked by this user",
            status_code=400,
        )
    else:
        try:
            collection.insert_one(data.model_dump())
        except Exception as e:
            raise HTTPException(
                detail=(e),
                status_code=500,
            )

async def save_wallet_details(id):
  # Todo:
  # checks if the wallet is already being tracked, else fetch data and add to the tracked-wallet
  print("holla")

async def get_wallet_details():
  pass


def group_by_id(data):
    grouped = defaultdict(list)
    for item in data:
        grouped[item["id"]].append(item["email"])
    return [
      {"id": id_, "emails": emails} for id_, emails in grouped.items()
    ]

async def fetch_wallet_data():
  print("fetch data")
  client = await get_client()
  database = client["defi-db"]
  collection = database["wallet-track"]
  results = collection.find({}).to_list(length=None)
  if results:
    results = group_by_id(results)
  #print(results)
  for r in results:
    d = await all_user_data_without_fills(r["id"])
    if d:
      print(d)
      # get_wallet_details()
      # compare data
      # if diff
      # send email
      # save the new data
  