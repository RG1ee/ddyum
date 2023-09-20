from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routers import router as auth_router
from src.users.routers import router as user_router
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
