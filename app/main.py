from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .routers import post, user, authentication, vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)


@app.get("/")
def root():
  return {"message":"Hello world"}