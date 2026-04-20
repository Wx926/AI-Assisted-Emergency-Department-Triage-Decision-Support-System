from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from database import create_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to the ER Triage System"}