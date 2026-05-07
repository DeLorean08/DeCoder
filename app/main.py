from fastapi import FastAPI, Request
from app.api.v1.endpoints import auth, user, problem
from app.core.logging_config import logging, setup_logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles


setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="DeCoder")
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(problem.router)
template_dir = Path(__file__).parent / "frontend" / "templates"
templates = Jinja2Templates(directory=template_dir)
static_dir = Path(__file__).parent / "frontend" / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(request: Request):
    logger.info("Application DeCoder is starting up...")
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})
