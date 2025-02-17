from time import time
from typing import List, Optional
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# Imports models for all databases from models.py
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='root',
                                cursor_factory=RealDictCursor)  # Returns attribute name
        cursor = conn.cursor()
        print("Database connection succesful!")
        break
    except Exception as error:
        print("Database connection failed.")
        print("Error: ", error)
        time.sleep(2)


# my_posts = [{"title": "title of post ",
#             "content": "content of post 1",
#              "id": 1
#              },
#             {"title": "favorite foods",
#             "content": "I like pizza",
#              "id": 2
#              }
#             ]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

app.include_router(post.router)  # Imports post.py paths
app.include_router(user.router)  # Imports user.py paths
app.include_router(auth.router)  # Imports auth.py paths


@app.get("/")  # decorator that makes the function into a path operation
def root():
    # FastAPI sends this to browser as JSON
    return {"message": "Welcome to my API!"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):

#     # cursor.execute("""SELECT * FROM posts""")
#     posts = db.query(models.Post).all()
#     print(posts)
#     return {"data": "successful"}
