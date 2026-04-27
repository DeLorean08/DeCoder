from fastapi import FastAPI
from app.api.v1.endpoints import auth
from app.core.logging_config import logging, setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="DeCoder")
app.include_router(auth.router)

@app.get("/")
def read_root():
    logger.info("Application DeCoder is starting up...")
    return {"message": "Hello from decoder!"}
