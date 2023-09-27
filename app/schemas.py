from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

#request
class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True


class PostCreate(PostBase):
  pass

#request users table
class UserCreate(BaseModel):
  email: EmailStr
  password: str


#response user
class UserOut(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  class Config:
    from_attributes = True

#response 
class PostRes(PostBase):
  id: int
  created_at: datetime
  owner_id: int
  owner: UserOut
  # title: str
  # content: str
  # published: bool
  # these there are inherited from PostBase class

  class Config:
    from_attributes = True
    # orm_mode

#after joins post output
class PostOut(PostBase):
  Post: PostRes
  votes: int
  class Config:
    from_attributes = True


#authentication
class UserLogin(BaseModel):
  email: EmailStr
  password: str


#token request
class Token(BaseModel):
  access_token: str
  token_type: str

#token response
class TokenData(BaseModel):
  id: Optional[int] = None


# vote request
class VoteReq(BaseModel):
  post_id: int
  dir: conint(le=1) 