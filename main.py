from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": "posts"}

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    print(post.title)
    print(post.dict())
    return {"data": "post"}

@app.get("/posts/latest")
def get_latest_post():
    # get latest post from data source 
    return {"post details": f"Here is post {id}"}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    print(id)
    return {"post details": f"Here is post {id}"}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
