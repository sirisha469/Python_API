from fastapi import status, HTTPException, Depends, FastAPI, Response, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
  prefix="/users"
)

# users table

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):

  #hash the password - user.password
  # hashed_password = pwd_context.hash(user.password)

  hashed_password = utils.hash(user.password)
  user.password = hashed_password

  new_user = models.User(**user.model_dump())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user


#getting user by id
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

  user = db.query(models.User).filter(models.User.id == id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"user with id;{id} does not exists")

  return user
  