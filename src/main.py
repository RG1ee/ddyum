from fastapi import FastAPI

from src.auth.routers import router as auth_router


app = FastAPI(title="API FOR BOOKING PHOTO SHOOTS")

app.include_router(auth_router)
