from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database setup
engine = create_engine("sqlite:///metrics.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Table model
class MetricsDB(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    cpu = Column(Float)
    memory = Column(Float)
    time = Column(DateTime)

# Create table
Base.metadata.create_all(bind=engine)

# Request model
class Metrics(BaseModel):
    cpu: float
    memory: float

# POST API → Save to DB
@app.post("/metrics")
def add_metrics(data: Metrics):
    db = SessionLocal()

    new_entry = MetricsDB(
        cpu=data.cpu,
        memory=data.memory,
        time=datetime.now()
    )

    db.add(new_entry)
    db.commit()
    db.close()

    return {"message": "Saved to database"}

# GET API → Read from DB
@app.get("/metrics")
def get_metrics():
    db = SessionLocal()
    data = db.query(MetricsDB).all()
    db.close()
    return data

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)