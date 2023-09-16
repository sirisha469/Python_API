from pydantic import BaseModel
from datetime import datetime

#request
class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True


class PostCreate(PostBase):
  pass


#response 
class PostRes(PostBase):
  id: int
  created_at: datetime
  # title: str
  # content: str
  # published: bool
  # these there are inherited from PostBase class

  class Config:
    from_attributes = True
    # orm_mode