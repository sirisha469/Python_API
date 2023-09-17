from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

from .routers import post, user, authentication


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



#postgres database connection

while True:
  try:
    conn = psycopg2.connect(host='localhost', database='py_fastapi', user='postgres', password='0000', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful!")
    break

  except Exception as error:
    print("connecting to database failed")
    print("Error:", error)
    time.sleep(2)



@app.get("/")
def root():
  return {"message": "Hello World!!!"}

# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):

#   posts = db.query(models.Post).all()
#   return {"data": posts}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
