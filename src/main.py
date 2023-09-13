from fastapi import FastAPI

from src.users.routers import router as user_router


app = FastAPI(title="API FOR BOOKING PHOTO SHOOTS")

app.include_router(user_router)
