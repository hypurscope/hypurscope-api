import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.helper.defi_functions import my_periodic_task
from src.routes import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(my_periodic_task())
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
