from fastapi import FastAPI
from app.routers import version_checker

app = FastAPI()

app.include_router(version_checker.router)
