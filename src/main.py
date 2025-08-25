import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.helper.defi_functions import my_periodic_task
from src.routes import routes
from src.helper.functions import fetch_wallet_data
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(
  fetch_wallet_data,
  "interval",
  seconds=30,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(my_periodic_task())
    scheduler.start()
    # print("📡 Broadcast task started")
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)
app.include_router(routes.router)
