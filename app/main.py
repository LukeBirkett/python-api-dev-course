from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
  
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='postgres', 
            password='Torrent123!!!', 
            cursor_factory=RealDictCursor
            )
        cursor = conn.cursor()
        print("database connected")
        break
    except Exception as error:
        print("database connect failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [
    {"title": "title1", "content": "content1", "id": 1},
    {"title": "title2", "content": "content2", "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalch")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"return": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # RAW SQL METHOD
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
        (post.title, post.content, post.published)
        )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id)))
    deleted = cursor.fetchone()
    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
        (post.title, post.content, post.published, str(id))
        )
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    conn.commit()
    return{"message": updated_post}