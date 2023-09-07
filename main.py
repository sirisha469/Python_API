from fastapi import Body, FastAPI
from pydantic import BaseModel, PostgresDsn

app = FastAPI()

# request get method url: "/"

class Post(BaseModel):
  title: str
  content: str

@app.get("/")
def root():
  return {"message": "Hello World!!!"}

@app.get("/posts")
def get_posts():
  return {"data": "This is your post"}

# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#   #print(payLoad)
#   return {
#     "message": "successfully create post", 
#     "new_post": f"title {payLoad['title']} content {payLoad['content']}"
#   }

@app.post("/createposts")
def create_posts(new_post: Post):
  print(new_post)
  return {"data": "new post"}

