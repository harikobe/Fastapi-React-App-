from fastapi import FastAPI,HTTPException,Depends
from typing import Annotated,List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal,engine
import models
#MiddleWare
from  fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
     "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#pydantic models:
class TransactionBase(BaseModel):
     amount:float
     category:str
     description:str
     is_income:bool
     date:str
     
class TransactionModel(TransactionBase):
     id:int
     
     class Config:
          orm_mode = True
          
          
     
#db dependency: provide the db session for the fastapi routes
def get_db():
     db= SessionLocal()
     try:
          yield db
     finally:
          db.close()
          

#for the sync with the models and db
models.Base.metadata.create_all(bind=engine)


@app.post("/transactions/",response_model=TransactionModel)
async def create_transaction(transaction:TransactionBase,db:Session = Depends(get_db)):
     db_transaction = models.Transaction(**transaction.dict())
     db.add(db_transaction)
     db.commit()
     db.refresh(db_transaction)
     return db_transaction


@app.get("/transactions/",response_model=List[TransactionModel])
async def get_transactions(db: Session=Depends(get_db),skip:int=0,limit:int=0):
          transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
          return transactions
     
     