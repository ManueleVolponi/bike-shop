from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from server.controllers import api_configurator
import os

load_dotenv()

app = FastAPI()

origins_raw = os.getenv("ORIGINS", "")
origins_list = origins_raw.split(",") if origins_raw else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_configurator.router)