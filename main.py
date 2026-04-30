from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from database import engine

app = FastAPI()

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class MetricsDB(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    cpu = Column(Float)
    memory = Column(Float)
    time = Column(DateTime)

Base.metadata.create_all(bind=engine)

# Request model
class Metrics(BaseModel):
    cpu: float
    memory: float

# POST API
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

    return {"message": "Saved"}

# GET API
@app.get("/metrics")
def get_metrics():
    db = SessionLocal()
    data = db.query(MetricsDB).all()
    db.close()
    return data

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)