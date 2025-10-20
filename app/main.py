from fastapi import FastAPI

from app.routes import wallet_router

app = FastAPI()
app.include_router(wallet_router)
