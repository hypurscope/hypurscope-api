import asyncio

from fastapi import HTTPException
from src.helper.functions import process_defi, save_or_update_defi_to_db


clients = set()


async def notify_clients():
    try:
        value = await process_defi()
        await save_or_update_defi_to_db(updated_data=value)

        dead_clients = []
        for ws in list(clients):
            try:
                await ws.send_text(value.model_dump_json())
            except Exception as e:
                dead_clients.append(ws)
                # print(f"error: {str(e)}")
                raise HTTPException(details=str(e))

        for ws in dead_clients:
            clients.discard(ws)

    except Exception as e:
        # print(f"Error in notify_clients: {e}")
        raise HTTPException(details=f"Error in notify_clients: {e}")


async def my_periodic_task():
    while True:
        await notify_clients()
        await asyncio.sleep(30)
