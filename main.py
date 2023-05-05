from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DatabaseError

# Database connection string
SQLALCHEMY_DATABASE_URL = "sqlite:///./phonebook.db"

# Create SQLALchemy engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy model
Base = declarative_base()

# Define PhoneBook model
class PhoneBook(Base):
    __tablename__ = "phonebook"
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    phone_number = Column(String, index=True)

# Create database tables
Base.metadata.create_all(bind=engine)

# Pydantic model for input data
class PhoneBookInput(BaseModel):
    fullname: str
    phone_number: str

# Pydantic model for output data
class PhoneBookOutput(BaseModel):
    id: int
    fullname: str
    phone_number: str
    
    class Config:
        orm_mode = True

app = FastAPI()

# add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add data to phonebook
@app.post("/phonebook/add", response_model=PhoneBookOutput)
async def add_phonebook_entry(phonebook: PhoneBookInput, db = Depends(get_db)):
    try:
        db_entry = PhoneBook(fullname=phonebook.fullname, phone_number=phonebook.phone_number)
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return PhoneBookOutput.from_orm(db_entry)
    except DatabaseError as e:
        return {"error": str(e)}

# Get all entries from phonebook
@app.get("/phonebook", response_model=List[PhoneBookOutput])
async def get_phonebook(db = Depends(get_db)):
    return db.query(PhoneBook).all()
