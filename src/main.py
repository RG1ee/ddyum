from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.auth.routers import router as auth_router
from src.users.routers import router as user_router
from src.bookings.routers import router as booking_router
from src.config.settings import settings


app = FastAPI(title="API FOR BOOKING PHOTO SHOOTS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(user_router, prefix=settings.API_PREFIX)
app.include_router(booking_router, prefix=settings.API_PREFIX)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        f"{settings.CACHE_DSN}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
