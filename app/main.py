from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .routers import post, user, authentication, vote
from .config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)
