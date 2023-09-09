from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()

# request get method url: "/"

class Post(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = None




my_posts = [
  {"title": "title of post 1", "content": "content of post 1", "id":1},
  {"title": "favorite food", "content": "I like papidi", "id":2}
]


#getting specified ID
def find_post(id):
  for p in my_posts:
    if p['id'] == id:
      return p
    

#getting specified index
def find_index_post(id):
  for index, p in enumerate(my_posts):
    if p['id'] == id:
      return index
    


@app.get("/")
def root():
  return {"message": "Hello World!!!"}

#read: getting all posts
@app.get("/posts")
def get_posts():
  return {"data": my_posts}

# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#   #print(payLoad)
#   return {
#     "message": "successfully create post", 
#     "new_post": f"title {payLoad['title']} content {payLoad['content']}"
#   }

#create: creating posts 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
  # print(post.rating)
  # print(post)
  # print(post.model_dump())
  #model_dump is a dictionary


  #id is not there in Post class so we want to create 
  post_dict = post.model_dump()
  post_dict['id'] = randrange(0, 100000)
  my_posts.append(post_dict)
  return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
  post = my_posts[len(my_posts)-1]
  return {"details": post}



#read: getting single post based on id
@app.get("/posts/{id}")
def get_post(id: int, response: Response): 
  #id: int it default takes the id as integer no need of explicit conversion
  print(id)
  print(type(id)) 
  #here id is a string but our method wants a integer so convert that string into integer
  #for this we are creating a method(find_post())
  #post = find_post(int(id))

  post = find_post(id)
  print(post)
  if not post:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
    # the above code is used to replace the below 2 lines by using this we can also remove the parameter of the method response: Response
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id: {id} was not found"}
  return {"single data": post }


#delete: deleting post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  #find the index in the array that has required ID
  #my_posts.pop(index)

  index = find_index_post(id)

  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
  my_posts.pop(index)
  #return {"message": "post successfully deleted"}
  return Response(status_code=status.HTTP_204_NO_CONTENT)


#update post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  index = find_index_post(id)

  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
  
  post_dict = post.model_dump()
  post_dict['id'] = id
  my_posts[index] = post_dict
  print(post_dict)
  return {"data": post_dict}
  