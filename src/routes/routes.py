import asyncio
from datetime import datetime
from typing import Optional
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    WebSocket,
    WebSocketDisconnect,
)
from src.helper.db import get_client  # noqa: F401
from src.helper.defi_functions import clients
from src.validator.defi import Protocol
from src.helper.functions import (
    process_defi,
    get_defi_from_db,
)
from src.helper.user_functions import all_user_data
from src.helper.hyperscan_function import get_spot_in_usdc, get_token_holders

router = APIRouter(prefix="/api")


@router.websocket("/get-defi")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        try:
            # Send initial data immediately
            initial_data = await get_defi_from_db()
            initial_data = Protocol.model_validate(initial_data)
            await websocket.send_text(initial_data.model_dump_json())
        except Exception as db_err:
            # Send DB error instead of killing WS
            await websocket.send_text(
                f'{{"error": "DB fetch failed: {db_err}"}}',
            )

        # Keep connection alive by waiting indefinitely
        # Periodic updates from notify_clients will keep the socket active
        while True:
            await asyncio.sleep(3600)  # Long sleep to minimize CPU usage

    except WebSocketDisconnect:
        pass
    except Exception as e:
        raise HTTPException(details=f"WebSocket error: {e}")
    finally:
        clients.discard(websocket)


def validate_datetime_format(value: Optional[str], required: bool = False):
    if value is None:
        if required:
            raise HTTPException(
                status_code=400,
                detail="start_time is required and must be in 'YYYY-MM-DD HH:MM' format",
            )
        return None

    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="time must be in 'YYYY-MM-DD HH:MM' format and be a valid date/time",
        )
    return value


@router.get("/user-info/{id}")
async def user_info(
    id: str = Path(..., description="User ID"),
    start_time: str = Query(
        ...,
        description="Start time in 'YYYY-MM-DD HH:MM' format",
        alias="start_time",
        regex=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$",
    ),
    end_time: Optional[str] = Query(
        None,
        description="End time in 'YYYY-MM-DD HH:MM' format",
        alias="end_time",
        regex=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$",
    ),
):
    # Validate with custom function
    start_time = validate_datetime_format(start_time, required=True)
    end_time = validate_datetime_format(end_time)
    # Call your function
    value = all_user_data(id=id, start_time=start_time, end_time=end_time)
    return value


@router.get("/defi")
async def defi_data():
    value = await process_defi()
    try:
        client = await get_client()
        database = client["defi-db"]
        collection = database["defi"]
        collection.insert_one(value.model_dump())
    except Exception as e:
        raise HTTPException(details=str(e))
    finally:
        return value


@router.get("/get-holder/{token}")
async def get_holders(token: str):
    return await get_token_holders(token)


@router.get("/get-spot-info")
async def get_spot_info():
    return await get_spot_in_usdc()
