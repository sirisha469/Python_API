from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# request get method url: "/"

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

#read: getting all posts
@app.get("/posts")
def get_posts():
  cursor.execute(""" SELECT * FROM posts  """)
  post = cursor.fetchall()
  return {"data": post}

#create: creating posts 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
  
  cursor.execute(""" INSERT INTO posts(title, content, published) values(%s, %s, %s) returning *""", (post.title, post.content, post.published))

  new_post = cursor.fetchone()

  conn.commit()
  
  return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
  post = my_posts[len(my_posts)-1]
  return {"details": post}



#read: getting single post based on id
@app.get("/posts/{id}")
def get_post(id: str): 
  cursor.execute(""" SELECT * from posts WHERE id = %s """, (id))
  post = cursor.fetchone()

  print(post)
  if not post:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  return {"single data": post }


#delete: deleting post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
  cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (id))
  deleted_post = cursor.fetchone()
  conn.commit()

  if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)


#update post
@app.put("/posts/{id}")
def update_post(id: str, post: Post):

  cursor.execute(""" UPDATE posts SET title=%s , content=%s, published=%s where id = %s returning *""", (post.title, post.content, post.published, id))

  updated_post = cursor.fetchone()
  conn.commit()

  if updated_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
  
 
  return {"data": updated_post}
  