from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mssql+pyodbc://@localhost/MonitorDB?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)