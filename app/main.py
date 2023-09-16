from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
  title: str
  content: str
  published: bool = True



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

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):

  posts = db.query(models.Post).all()
  return {"data": posts}

#read: getting all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
  # cursor.execute(""" SELECT * FROM posts  """)
  # post = cursor.fetchall()

  posts = db.query(models.Post).all()
  return {"data": posts}

#create: creating posts 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
  
  # cursor.execute(""" INSERT INTO posts(title, content, published) values(%s, %s, %s) returning *""", (post.title, post.content, post.published))

  # new_post = cursor.fetchone()

  # conn.commit()

  # print(**post.dict())

  # new_post = models.Post(title=post.title, content= post.content, published= post.published)

  new_post = models.Post(**post.model_dump())
  
  db.add(new_post)
  db.commit()
  db.refresh(new_post)

  return {"data": new_post}



#read: getting single post based on id
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)): 
  # cursor.execute(""" SELECT * from posts WHERE id = %s """, (id))
  # post = cursor.fetchone()

  # print(post)

  post = db.query(models.Post).filter(models.Post.id == id).first()
  # print(post)

  if not post:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  return {"single data": post }


#delete: deleting post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  # cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (id))
  # deleted_post = cursor.fetchone()
  # conn.commit()

  post = db.query(models.Post).filter(models.Post.id == id)

  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
  
  post.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)


#update post
@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):

  # cursor.execute(""" UPDATE posts SET title=%s , content=%s, published=%s where id = %s returning *""", (post.title, post.content, post.published, id))

  # updated_post = cursor.fetchone()
  # conn.commit()

  post_query = db.query(models.Post).filter(models.Post.id == id)

  post = post_query.first()

  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
  
  post_query.update(post.dict(), synchronize_session=False)

  db.commit()

  return {"data": post_query.first()}
  